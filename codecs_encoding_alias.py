#!/usr/bin/env python3
## -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:
##
## SPDX-FileCopyrightText: 2025 SATOH Fumiyasu @ OSSTech Corp., Japan
## SPDX-License-Identifier: GPL-3.0-or-later

import codecs
import encodings


def encoding_alias(alias, encoding_name):
    encoding = codecs.lookup(encoding_name)
    alias_normalized = alias.lower().translate(str.maketrans({"-": "_", " ": "_"}))

    def _encoding_search(encoding_name):
        if encoding_name == alias_normalized:
            return encoding
        else:
            None

    codecs.register(_encoding_search)
    ## FIXME: 不要にできない?
    encodings._cache[alias_normalized] = encoding


if __name__ == '__main__':
    import base64

    encoding_alias('gb2312', 'gb18030')
    encoding_alias('windows-874', 'cp874')
    encoding_alias('cseuckr', 'euc-kr')

    d = 'QSBWIM34IMXMILP2IMrbICAgqEMgs8kgyMsg'  # Sampled from a spam mail :-)
    b = base64.b64decode(d)
    try:
        u1 = b.decode('gb2312')
    except UnicodeDecodeError as e:
        print(f'u1: error: {e}')
    else:
        print(f'u1: {u1}')

    try:
        u2 = b.decode('gb18030')
    except UnicodeDecodeError as e:
        print(f'u1: error2: {e}')
    else:
        print(f'u2: {u2}')
