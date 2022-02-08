#!/usr/bin/env python3
## -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:

import sys
import re

needle = re.compile(r'^(?!(fumiyas|fumiyas2):).')

for line in sys.stdin:
    if needle.search(line):
        print(line, end='')
