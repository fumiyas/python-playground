#!/usr/bin/env python3
## -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:

import sys
## Python 2
#import errno


try:
    with open("msg.txt") as f:
        for line in f:
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            print(line)
except FileNotFoundError as e:
    print('%s: WARNING: %s' % (__file__, e), file=sys.stderr)
## Python 2
#except IOError as e:
#    if e.errno == errno.ENOENT:
#        print >>sys.stderr, '%s: WARNING: %s' % (__file__, e)
#    else:
#        raise
