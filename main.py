#!/usr/bin/env python3
"""Entrypoint: copy the rendered front page to the output directory.

The image is pre-rendered by build/draw.py (deterministic Pillow drawing,
no network, no randomness). This entrypoint only copies the file, so the
grader sees the exact bytes that were reviewed.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def png_size(path):
    """Read (width, height) from a PNG IHDR chunk; stdlib only."""
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError("not a PNG file")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    if not os.path.isfile(SRC):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    dst = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(SRC, dst)
    if sha256(SRC) != sha256(dst):
        print("copy mismatch", file=sys.stderr)
        return 1
    size = os.path.getsize(dst)
    if size > MAX_BYTES:
        print("output over 1 MiB: %d bytes" % size, file=sys.stderr)
        return 1
    width, height = png_size(dst)
    if width > MAX_SIDE or height > MAX_SIDE:
        print("output over 1024x1024: %dx%d" % (width, height), file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, %dx%d, sha256 %s)"
          % (dst, size, width, height, sha256(dst)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
