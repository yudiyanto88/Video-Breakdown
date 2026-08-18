#!/usr/bin/env python3
"""Ambil metadata + caption sebuah video dan tulis transcript.md sesuai format Outputs/.

Pengganti skill `watch` untuk sesi cloud (Claude Code on the web), di mana skill itu
tidak tersedia. Butuh `yt-dlp` dan akses jaringan ke youtube.com.

    python3 scripts/fetch_transcript.py <url> [--channel "On-Chain Mind"]

Mencetak path folder output ke stdout supaya bisa dipakai langsung oleh pipeline.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = REPO_ROOT / "Outputs"

# Paragraf baru dimulai setelah minimal 25 detik DAN kalimat sudah selesai,
# atau dipaksa setelah 60 detik supaya tidak ada blok raksasa.
PARA_MIN_SECONDS = 25
PARA_MAX_SECONDS = 60


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def slugify(title: str) -> str:
    """Judul LENGKAP -> kebab-case. Tidak dipersingkat (lihat CLAUDE.md)."""
    s = title.lower()
    # Apostrof & ampersand dibuang, bukan diganti pemisah: "What's" -> "whats",
    # "Fear & Greed" -> "fear-greed" (lihat contoh di CLAUDE.md).
    s = re.sub(r"['\u2019&]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def fetch_metadata(url: str) -> dict:
    try:
        out = run(["yt-dlp", "--skip-download", "--no-warnings", "-J", url]).stdout
    except FileNotFoundError:
        raise SystemExit("ERROR: yt-dlp belum terpasang. Jalankan: pip install yt-dlp")
    except subprocess.CalledProcessError as e:
        if "403" in e.stderr and "proxy" in e.stderr.lower():
            raise SystemExit(
                "ERROR: youtube.com diblokir egress proxy environment ini.\n"
                "Set Network access = Custom di cloud environment dan izinkan:\n"
                "  www.youtube.com / youtube.com / youtu.be / *.googlevideo.com\n"
                "(centang juga 'Also include default list of common package managers'),\n"
                "lalu mulai sesi BARU — policy dikunci saat sesi dibuat."
            )
        raise SystemExit(f"ERROR: yt-dlp gagal ambil metadata.\n{e.stderr.strip()}")
    return json.loads(out)


def download_subs(url: str, workdir: Path) -> tuple[Path, str]:
    """Ambil subtitle English. Manual diprioritaskan, auto sebagai fallback.

    json3 dipilih duluan karena cue-nya sudah bersih — tidak ada rolling-window
    overlap seperti vtt auto-caption.
    """
    attempts = [
        (["--write-subs"], "manual"),
        (["--write-auto-subs"], "auto"),
    ]
    for flags, kind in attempts:
        try:
            run([
                "yt-dlp", "--skip-download", "--no-warnings",
                *flags, "--sub-langs", "en.*,en",
                "--sub-format", "json3/vtt",
                "-o", str(workdir / "sub.%(ext)s"), url,
            ])
        except subprocess.CalledProcessError:
            continue
        files = sorted(workdir.glob("sub*.json3")) + sorted(workdir.glob("sub*.vtt"))
        if files:
            return files[0], kind
    raise SystemExit("ERROR: tidak ada subtitle English (manual maupun auto) di video ini.")


def parse_json3(path: Path) -> list[tuple[float, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    cues = []
    for ev in data.get("events", []):
        segs = ev.get("segs")
        if not segs:
            continue
        text = "".join(s.get("utf8", "") for s in segs)
        text = text.replace("\n", " ").strip()
        if text:
            cues.append((ev.get("tStartMs", 0) / 1000.0, text))
    return cues


def parse_vtt(path: Path) -> list[tuple[float, str]]:
    """Fallback: vtt auto-caption punya rolling overlap, jadi baris diulang."""
    def to_secs(ts: str) -> float:
        h, m, s = ts.split(":")
        return int(h) * 3600 + int(m) * 60 + float(s.replace(",", "."))

    cues, start, buf, prev = [], None, [], ""
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if "-->" in line:
            if start is not None and buf:
                cues.append((start, " ".join(buf)))
            start, buf = to_secs(line.split("-->")[0].strip().split()[0]), []
            continue
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        # Buang baris yang persis mengulang baris sebelumnya (overlap window).
        if line and line != prev:
            buf.append(line)
            prev = line
    if start is not None and buf:
        cues.append((start, " ".join(buf)))
    return cues


def to_paragraphs(cues: list[tuple[float, str]]) -> list[tuple[float, str]]:
    paras, start, words = [], None, []
    for t, text in cues:
        if start is None:
            start = t
        words.append(text)
        elapsed = t - start
        joined = " ".join(words).strip()
        ends_sentence = joined.endswith((".", "!", "?"))
        if (elapsed >= PARA_MIN_SECONDS and ends_sentence) or elapsed >= PARA_MAX_SECONDS:
            paras.append((start, re.sub(r"\s+", " ", joined)))
            start, words = None, []
    if words:
        paras.append((start or 0.0, re.sub(r"\s+", " ", " ".join(words).strip())))
    return paras


def hhmm(seconds: float) -> str:
    total = int(seconds)
    h, m, s = total // 3600, (total % 3600) // 60, total % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--channel", help="Override nama channel kalau metadata tidak rapi")
    args = ap.parse_args()

    meta = fetch_metadata(args.url)
    title = meta["title"]
    channel = args.channel or meta.get("channel") or meta.get("uploader") or "(tidak diketahui)"
    upload = meta.get("upload_date", "")
    date = f"{upload[:4]}-{upload[4:6]}-{upload[6:8]}" if len(upload) == 8 else "unknown-date"
    webpage = meta.get("webpage_url", args.url)

    folder = OUTPUTS / f"{date}_{slugify(title)}"
    folder.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        sub_path, kind = download_subs(args.url, Path(tmp))
        cues = parse_json3(sub_path) if sub_path.suffix == ".json3" else parse_vtt(sub_path)

    if not cues:
        raise SystemExit("ERROR: file subtitle terambil tapi kosong setelah di-parse.")

    source = "YouTube captions (auto), dibersihkan dari duplikasi overlap" if kind == "auto" \
        else "YouTube captions (manual/uploader)"

    body = "\n\n".join(f"[{hhmm(t)}] {text}" for t, text in to_paragraphs(cues))
    (folder / "transcript.md").write_text(
        f"# Transcript — {title}\n\n"
        f"**Channel:** {channel}\n"
        f"**URL:** {webpage}\n"
        f"**Tanggal video:** {date}\n"
        f"**Durasi:** {hhmm(meta.get('duration') or 0)}\n"
        f"**Sumber transkrip:** {source}\n\n"
        f"---\n\n{body}\n",
        encoding="utf-8",
    )
    print(folder.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
