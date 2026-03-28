#!/usr/bin/env python3

from pathlib import Path
import re
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: update_buf_release_version.py <tag>", file=sys.stderr)
        return 1

    tag = sys.argv[1].strip()
    if not tag:
        print("tag must not be empty", file=sys.stderr)
        return 1

    buf_yaml = Path("buf.yaml")
    content = buf_yaml.read_text(encoding="utf-8")
    pattern = re.compile(r"^# release_version: .*$", re.MULTILINE)
    replacement = f"# release_version: {tag}"

    if pattern.search(content):
        updated = pattern.sub(replacement, content, count=1)
    else:
        updated = f"{replacement}\n{content}"

    buf_yaml.write_text(updated, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
