"""Regenerates hero.svg and stack.svg. Usage: python assets/generate.py"""
import math
import random
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

W, H, CELL = 1280, 340, 5
COLS, ROWS = W // CELL, H // CELL
TITLE, TAGLINE = "JEREMY ZHAO", "I make games and simulations"
SAND = ["#fff0b8", "#ffdf8a", "#ffc861", "#ffab45", "#f58a35"]
DUNE = ["#c96f32", "#a9552b", "#864026", "#652f22", "#48241f"]
STACK = ["Unity", "Godot", "C#", "C++", "GDScript", "HLSL", "Python", "Rust", "TypeScript", "Java"]

FONT = {
    "A": "01110 10001 10001 11111 10001 10001 10001",
    "E": "11111 10000 10000 11110 10000 10000 11111",
    "H": "10001 10001 10001 11111 10001 10001 10001",
    "I": "11111 00100 00100 00100 00100 00100 11111",
    "J": "00111 00010 00010 00010 00010 10010 01100",
    "M": "10001 11011 10101 10101 10001 10001 10001",
    "O": "01110 10001 10001 10001 10001 10001 01110",
    "R": "11110 10001 10001 11110 10100 10010 10001",
    "Y": "10001 10001 01010 00100 00100 00100 00100",
    "Z": "11111 00001 00010 00100 01000 10000 11111",
    "a": "00000 00000 01110 00001 01111 10001 01111",
    "d": "00001 00001 01101 10011 10001 10001 01111",
    "e": "00000 00000 01110 10001 11111 10000 01110",
    "g": "00000 00000 01111 10001 01111 00001 01110",
    "i": "00100 00000 01100 00100 00100 00100 01110",
    "k": "10000 10000 10010 10100 11000 10100 10010",
    "l": "01100 00100 00100 00100 00100 00100 01110",
    "m": "00000 00000 11010 10101 10101 10001 10001",
    "n": "00000 00000 10110 11001 10001 10001 10001",
    "o": "00000 00000 01110 10001 10001 10001 01110",
    "s": "00000 00000 01111 10000 01110 00001 11110",
    "t": "01000 01000 11100 01000 01000 01001 00110",
    "u": "00000 00000 10001 10001 10001 10011 01101",
    " ": "00000 00000 00000 00000 00000 00000 00000",
}


def text_cells(text, scale, left, top):
    """Yield the grid cells covered by text in the 5x7 pixel font."""
    for i, char in enumerate(text):
        for y, row in enumerate(FONT[char].split()):
            for x, bit in enumerate(row):
                if bit == "1":
                    for dx in range(scale):
                        for dy in range(scale):
                            yield left + (i * 6 + x) * scale + dx, top + y * scale + dy


def falling_paths(grains):
    """Batch (x, y, color, delay) grains into one animated path per color and delay."""
    batches = defaultdict(list)
    for x, y, color, delay in grains:
        batches[color, round(delay / 0.05) * 0.05].append(f"M{x * CELL} {y * CELL}h{CELL}v{CELL}h-{CELL}z")
    return "".join(
        f'<path class="f" fill="{color}" style="animation-delay:{delay:.2f}s" d="{"".join(d)}"/>'
        for (color, delay), d in sorted(batches.items(), key=lambda item: item[0][1])
    )


def hero():
    rng = random.Random(7)
    grains = []
    for x in range(COLS):
        height = int(10 + 4 * math.sin(x / 23 + 1) + 2.5 * math.sin(x / 9) + rng.random() * 1.4)
        for depth in range(height):
            shade = min(len(DUNE) - 1, depth // 3 + (rng.random() < 0.22))
            grains.append((x, ROWS - height + depth, DUNE[shade], 0.1 + (height - depth) * 0.045 + rng.random() * 0.45))

    scale = 3
    left = (COLS - (len(TITLE) * 6 - 1) * scale) // 2
    top = 11
    for x, y in text_cells(TITLE, scale, left, top):
        band = (y - top) / (7 * scale) * (len(SAND) - 1)
        color = SAND[min(len(SAND) - 1, max(0, int(band + rng.uniform(-0.5, 0.7))))]
        grains.append((x, y, color, 1.1 + (top + 21 - y) * 0.075 + x / COLS * 0.55 + rng.random() * 0.3))

    tag_px = 3
    tag_left = (W - (len(TAGLINE) * 6 - 1) * tag_px) // 2
    tagline = "".join(
        f"M{tag_left + x * tag_px} {186 + y * tag_px}h{tag_px}v{tag_px}h-{tag_px}z"
        for x, y in text_cells(TAGLINE, 1, 0, 0)
    )
    stars = "".join(
        f'<rect class="s" x="{rng.randrange(W) // CELL * CELL}" y="{rng.randrange(230) // CELL * CELL}" '
        f'width="3" height="3" style="animation-delay:{rng.random() * 5:.1f}s"/>'
        for _ in range(46)
    )
    drift = "".join(
        f'<rect class="d" x="{rng.randrange(W)}" y="{rng.randrange(205, 285)}" width="4" height="4" '
        f'fill="{rng.choice(SAND)}" style="animation-delay:{rng.random() * 7 + 4:.1f}s"/>'
        for _ in range(22)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        f'aria-label="{TITLE.title()}: {TAGLINE}">'
        f"<title>{TITLE.title()}: {TAGLINE}</title>"
        '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#090d1f"/><stop offset=".55" stop-color="#1e1838"/>'
        '<stop offset=".85" stop-color="#57304f"/><stop offset="1" stop-color="#8c4a45"/></linearGradient>'
        f'<clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>'
        "<style>"
        ".f{animation:f .85s cubic-bezier(.55,0,1,.65) backwards}"
        f"@keyframes f{{from{{transform:translateY(-{H + 40}px)}}to{{transform:none}}}}"
        ".t{animation:t .8s 3.5s ease-out backwards}@keyframes t{from{opacity:0}to{opacity:1}}"
        ".s{fill:#dfe6ff;opacity:.55;animation:s 5s ease-in-out infinite}"
        "@keyframes s{50%{opacity:.08}}"
        ".d{opacity:0;animation:d 7s linear infinite}"
        "@keyframes d{0%{opacity:0;transform:none}15%{opacity:.8}100%{opacity:0;transform:translate(150px,-34px)}}"
        "@media (prefers-reduced-motion:reduce){.f,.t,.s,.d{animation:none}}"
        "</style>"
        f'<g clip-path="url(#card)"><rect width="{W}" height="{H}" fill="url(#sky)"/>{stars}'
        f'{falling_paths(grains)}<path class="t" fill="#f6d9a8" d="{tagline}"/>{drift}</g></svg>'
    )


def stack():
    size, pad, gap, height = 15, 15, 9, 34
    widths = [round(len(name) * size * 0.61) + pad * 2 for name in STACK]
    total = sum(widths) + gap * (len(STACK) - 1)
    x, chips = 0, ""
    for i, (name, width) in enumerate(zip(STACK, widths)):
        color = SAND[i % len(SAND)]
        chips += (
            f'<rect x="{x + .5}" y=".5" width="{width - 1}" height="{height - 1}" rx="7" fill="#17152b" stroke="{color}"/>'
            f'<text x="{x + width / 2}" y="22.5" text-anchor="middle" fill="{color}">{name}</text>'
        )
        x += width + gap
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total} {height}" width="{total}" height="{height}" '
        f'role="img" aria-label="Tech stack: {", ".join(STACK)}"><title>Tech stack</title>'
        f'<g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,Liberation Mono,monospace" '
        f'font-size="{size}" font-weight="700">{chips}</g></svg>'
    )


if __name__ == "__main__":
    out = Path(__file__).parent
    for name, svg in (("hero.svg", hero()), ("stack.svg", stack())):
        ET.fromstring(svg)  # must stay well-formed
        assert len(svg) < 400_000, f"{name} is too large for a README image"
        (out / name).write_text(svg, encoding="utf-8")
        print(name, len(svg) // 1024, "KB")
