#!/usr/bin/env python3
"""Copy the stored one-line pitch to the grader's output directory.

Stdlib only: the grading sandbox has no third-party packages and the
repository is mounted read-only, so this script never writes into the
repo and never imports anything beyond the standard library.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.txt"
OUTPUT_NAME = "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 240


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, OUTPUT_NAME)

    with open(source, "rb") as handle:
        data = handle.read()
    text = data.decode("utf-8")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS) or not text.strip():
        print(f"entry must be {MIN_CHARS}-{MAX_CHARS} non-blank chars, got {len(text)}", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    if not os.path.isdir(out_dir):
        print(f"output dir {out_dir} is not a directory", file=sys.stderr)
        return 1
    try:
        shutil.copyfile(source, target)
    except shutil.SameFileError:
        pass
    if _sha256(source) != _sha256(target):
        print("copy mismatch: output differs from source", file=sys.stderr)
        return 1
    print(f"wrote {OUTPUT_NAME} ({len(text)} chars, sha256 {_sha256(target)[:12]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
