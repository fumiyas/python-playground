#!/usr/bin/env python3
## -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:

import sys
import ldap
import ldap.asyncsearch


def result(s):
    try:
        partial = s.processResults()
    except ldap.SIZELIMIT_EXCEEDED:
        sys.stderr.write('Warning: Server-side size limit exceeded.\n')
    else:
        if partial:
            sys.stderr.write('Warning: Only partial results received.\n')

    sys.stdout.write(
        '%d results received.\n' % (
            len(s.allResults)
        )
    )


l = ldap.initialize('ldap://ldap.example.co.jp')
s1 = ldap.asyncsearch.List(l)
s2 = ldap.asyncsearch.List(l)

s1.startSearch(
    'dc=example,dc=co,dc=jp',
    ldap.SCOPE_SUBTREE,
    '(objectClass=*)',
)
s2.startSearch(
    'dc=example,dc=co,dc=jp',
    ldap.SCOPE_SUBTREE,
    '(objectClass=xxxxxx)',
)

result(s2)
result(s1)
