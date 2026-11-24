"""precommit.py: the key check git runs before every commit in a team repo.

setup.py installs a small pre-commit hook that runs this file. Team repos are
private, so GitHub's free secret scanning no longer catches a key that reaches
one: this is the check that does. It looks only at what is staged, prints the
file and line (never the key, only its last four characters), and refuses the
commit. If git cannot say what is staged, it lets the commit through: a check
that cannot run must never stop someone's work.
"""

from __future__ import annotations

import os
import sys

import importlib.util

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _keyscan():
    """keyscan.py on its own, by path. Importing the support package would pull in
    the SDK, and the hook may run on a Python without it: that import failing would
    quietly let every commit through."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keyscan.py")
    spec = importlib.util.spec_from_file_location("larkspur_keyscan", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    try:
        keyscan = _keyscan()
    except Exception:  # noqa: BLE001
        return 0
    hits = keyscan.staged(HERE)
    if not hits:
        return 0
    print("\nCommit stopped: a key to Claude is in what you are about to commit.", file=sys.stderr)
    for h in hits[:10]:
        print("  " + keyscan.where(h), file=sys.stderr)
    print("\nDelete the key from that file, save it, run `git add` on it again, then commit.\n"
          "The key belongs only in .env, which never goes to GitHub. If it was already\n"
          "pushed, tell your facilitator now.\n", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
