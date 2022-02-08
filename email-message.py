#!/usr/bin/env python
## -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:

from __future__ import print_function

import sys
import email

msg = email.message_from_file(sys.stdin)
print(msg.as_string())
