#!/usr/bin/env python3
## -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:

import sys


encoding = sys.argv[1]

b = sys.stdin.buffer.read()
print(f"bytes: {b!r}")
s = b.decode(encoding)
print(f"str:   {s!r}")
