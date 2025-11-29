"""Adds an alias to use the refactored function by default.
Run: python scripts/flip_refactor.py path/to/compliance.py
"""

import sys
import pathlib
import re


def main():
    if len(sys.argv) != 2:
        print("usage: python scripts/flip_refactor.py <file.py>")
        sys.exit(1)
    p = pathlib.Path(sys.argv[1])
    s = p.read_text(encoding="utf-8", errors="ignore")
    if "def check_pre_execution_refactored(" not in s:
        print("refactored function not found")
        sys.exit(2)
    if re.search(r"\bcheck_pre_execution\s*=\s*check_pre_execution_refactored\b", s):
        print("alias already present")
        return
    s += "\n# Use refactored implementation by default\ncheck_pre_execution = check_pre_execution_refactored\n"
    p.write_text(s, encoding="utf-8")
    print("✅ alias inserted")


if __name__ == "__main__":
    main()
