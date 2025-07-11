#!/usr/bin/env python3
## -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:

import sys
import re
from unicodedata import normalize
from unicodedata import combining

## U+0300 COMBINING GRAVE ACCENT .. U+036F COMBINING LATIN SMALL LETTER X
## U+3099 COMBINING KATAKANA-HIRAGANA VOICED SOUND MARK
## U+309A COMBINING KATAKANA-HIRAGANA SEMI-VOICED SOUND MARK
marks_re = re.compile('[\u0300-\u036f\u3099\u309A]')


def unmark_regex(text):
    s = normalize('NFD', text)
    s = marks_re.sub('', s)
    return normalize('NFC', s)


def unmark_combining(text):
    s = normalize('NFD', text)
    s = ''.join(c for c in s if not combining(c))
    return normalize('NFC', s)


print(unmark_regex(sys.argv[1]))
print(unmark_combining(sys.argv[1]))
