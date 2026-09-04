#!/usr/bin/env python3
"""Composite a rendered image sequence into a 4x4 flipbook sheet."""

from pathlib import Path

from PIL import Image

FRAME_SIZE = 256
COLS = 4
ROWS = 4
TARGET_FRAMES = COLS * ROWS

src_dir = Path(__file__).parent
out_path = src_dir / "confetti_flipbook_4x4_1024.png"

sources = sorted(src_dir.glob("confetti.png*.png"))
if not sources:
    raise SystemExit("no source frames found")

print(f"found {len(sources)} source frames")
with Image.open(sources[0]) as probe:
    print(f"source resolution {probe.size}, mode {probe.mode}")

# Evenly sample across the full sequence so the flipbook still covers the
# whole animation when the render has more frames than the sheet holds.
picked = [sources[round(i * (len(sources) - 1) / (TARGET_FRAMES - 1))] for i in range(TARGET_FRAMES)]

sheet = Image.new("RGBA", (COLS * FRAME_SIZE, ROWS * FRAME_SIZE), (0, 0, 0, 0))

for index, path in enumerate(picked):
    with Image.open(path) as frame:
        frame = frame.convert("RGBA")
        # Cells are square, so center-crop anything non-square rather than
        # stretching it, which would desync the flipbook from the render.
        if frame.width != frame.height:
            side = min(frame.size)
            left = (frame.width - side) // 2
            top = (frame.height - side) // 2
            frame = frame.crop((left, top, left + side, top + side))
        frame = frame.resize((FRAME_SIZE, FRAME_SIZE), Image.LANCZOS)
        col = index % COLS
        row = index // COLS
        # Straight paste, not alpha-composite, so premultiplied render alpha
        # is carried into the sheet untouched.
        sheet.paste(frame, (col * FRAME_SIZE, row * FRAME_SIZE))
    print(f"cell {index:2d} (row {row}, col {col}) <- {path.name}")

sheet.save(out_path)
print(f"wrote {out_path} ({sheet.size[0]}x{sheet.size[1]})")
