#!/usr/bin/env python3
"""Assemble fireball_loop_fb####.png frames into an 8x8 flipbook texture."""

from pathlib import Path

from PIL import Image

GRID = 8
OUTPUT_SIZE = 4096
CELL_SIZE = OUTPUT_SIZE // GRID
INPUT_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = INPUT_DIR / "fireball_loop_flipbook_4096.png"


def main() -> None:
    frames = sorted(INPUT_DIR.glob("fireball_loop_fb*.png"))
    if len(frames) != GRID * GRID:
        raise SystemExit(
            f"Expected {GRID * GRID} frames, found {len(frames)} in {INPUT_DIR}"
        )

    flipbook = Image.new("RGBA", (OUTPUT_SIZE, OUTPUT_SIZE))

    for index, frame_path in enumerate(frames):
        with Image.open(frame_path) as frame:
            if frame.size != (CELL_SIZE, CELL_SIZE):
                raise SystemExit(
                    f"{frame_path.name} is {frame.size[0]}x{frame.size[1]}, "
                    f"expected {CELL_SIZE}x{CELL_SIZE}"
                )
            frame_rgba = frame.convert("RGBA")
            col = index % GRID
            row = index // GRID
            flipbook.paste(frame_rgba, (col * CELL_SIZE, row * CELL_SIZE))

    flipbook.save(OUTPUT_PATH, optimize=False)
    print(f"Wrote {OUTPUT_PATH} ({OUTPUT_SIZE}x{OUTPUT_SIZE}, {len(frames)} frames)")


if __name__ == "__main__":
    main()
