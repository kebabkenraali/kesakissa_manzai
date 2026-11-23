# -*- coding: utf-8 -*-
"""Generoi äänet Kesäkissa-lyhytelokuvan vuoroille Microsoft Edge -neuroäänillä.

Käyttö: python generoi_aani.py
Tulokset: audio/line_00.mp3 ... (indeksi vastaa HTML:n LINES-taulukon riviä)
"""
import asyncio
import re
from pathlib import Path
from edge_tts.exceptions import NoAudioReceived

import edge_tts

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "kesakissa-lyhytelokuva.html"
OUT = ROOT / "audio"

VOICES = {
    "ÄITI": ("fi-FI-NooraNeural", "-4%", "+5Hz"),   # lämmin, hieman painava
    "POIKA": ("fi-FI-HarriNeural", "+4%", "+12Hz"),  # nuorempi, hieman korkeampi
}

ROW = re.compile(
    r"^\s*\['([^']*)','(.*?)','([^']*)'(?:,'([^']*)')?\],?\s*$",
    re.MULTILINE,
)


def lue_vuorot():
    src = HTML.read_text(encoding="utf-8")
    block = src.split("const LINES = [", 1)[1].split("\n];", 1)[0]
    rows = [m.groups() for m in ROW.finditer(block)]
    if len(rows) != 44:
        raise SystemExit(f"Odotettiin 44 vuoroa, löytyi {len(rows)}")
    return rows


async def generoi(idx, who, text, scene, sem):
    if who == "—":  # "(pieni tauko)" – ei ääntä
        return None
    voice, rate, pitch = VOICES[who]
    path = OUT / f"line_{idx:02d}.mp3"
    if path.exists() and path.stat().st_size > 1000:
        print(f"[{idx:02d}] ohitetaan (jo olemassa)", flush=True)
        return path
    async with sem:
        for attempt in range(1, 6):
            try:
                tts = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
                await tts.save(str(path))
                if path.exists() and path.stat().st_size > 1000:
                    break
                raise NoAudioReceived("tyhjä tiedosto")
            except NoAudioReceived:
                if attempt == 5:
                    raise
                await asyncio.sleep(1.5 * attempt)
    print(f"[{idx:02d}] {who:5s} {voice} -> {path.name} ({path.stat().st_size} B)", flush=True)
    return path


async def main():
    OUT.mkdir(exist_ok=True)
    rows = lue_vuorot()
    sem = asyncio.Semaphore(2)
    tasks = [generoi(i, r[0], r[1], r[2], sem) for i, r in enumerate(rows)]
    made = await asyncio.gather(*tasks)
    print(f"Valmis: {sum(1 for p in made if p)} äänitiedostoa hakemistossa {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
