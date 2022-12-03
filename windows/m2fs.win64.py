# coding: utf-8

import sys
import os

from m2fs.cli import main

c = main(sys.argv[1:])
os.system("pause")
sys.exit(c)
