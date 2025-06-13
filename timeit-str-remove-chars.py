#!/usr/bin/env python3
# -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:
#
# SPDX-FileCopyrightText: 20XX SATOH Fumiyasu @ OSSTech Corp., Japan
# SPDX-License-Identifier: GPL-3.0-or-later
#

import re
from timeit import timeit


text = r"""
ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz
"""

needle_re = re.compile("[Aa]")
needle_i_re = re.compile("A", re.IGNORECASE)

its = {
    "str.replace": lambda: text.replace("A", "").replace("a", ""),
    "str.translate": lambda: text.translate(str.maketrans("", "", "Aa")),
    "re.sub": lambda: re.sub("[Aa]", "", text),
    "re.compile / sub": lambda: needle_re.sub("", text),
    "re.compile(re.I) / sub": lambda: needle_i_re.sub("", text),
}   

for label, func in its.items():
    print(f"{label:<30}", timeit(func))
    print(func())
