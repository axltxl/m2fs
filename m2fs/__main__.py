# -*- coding: utf-8 -*-

import sys
from . import cli


def main() -> int:
    return cli.main(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
