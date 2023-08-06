import sys
import argparse
from pathlib import Path
from emptyfile.remover import Remover

def execute(args=None):
    if not args:
        if not sys.argv[1:]:
            args = ["-h"]
        else:
            args = sys.argv[1:]
    parser = argparse.ArgumentParser(
        "emptyfile",
        description="empty file remover"
    )
    parser.add_argument(
        "path",
        help="base directory and starting point.",
        nargs="+",
        action="store"
    )
    namespace = parser.parse_args(args)
    rem = Remover()
    for p in namespace.path:
        P = Path(p)
        rem.find_and_remove(P)
    return namespace
