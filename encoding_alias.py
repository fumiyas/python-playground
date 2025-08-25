#!/usr/bin/env python3
# -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:
#
# SPDX-FileCopyrightText: 2025 SATOH Fumiyasu @ OSSTech Corp., Japan
# SPDX-License-Identifier: GPL-3.0-or-later

import codecs
import encodings


_encoding_by_name = {}


def encoding_alias(alias, encoding_name):
    encoding = codecs.lookup(encoding_name)
    alias_encoding = codecs.CodecInfo(
        name=alias,
        encode=encoding.encode,
        decode=encoding.decode,
        streamreader=encoding.streamreader,
        streamwriter=encoding.streamwriter,
        incrementalencoder=encoding.incrementalencoder,
        incrementaldecoder=encoding.incrementaldecoder,
    )

    alias = alias.lower().replace('-', '_')  # lazy, but fast
    #alias = encodings.normalize_encoding(alias)  # strict, but slow

    _encoding_by_name[alias] = alias_encoding
    encodings._cache[alias] = None


def encoding_search(encoding_name):
    return _encoding_by_name.get(encoding_name)


codecs.register(encoding_search)


if __name__ == '__main__':
    import base64

    encoding_alias('shift_jis', 'cp932')
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
