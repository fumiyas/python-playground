#!/usr/bin/env python3
## -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:

import sys
import logging
from timeit import timeit

sys.stderr = open('/dev/null', 'w')

n = 1000000
s = "Foo"
i = 123

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)
print("1: formatted string, no output:", timeit(lambda: logger.info(f"Log: {s}: {i}"), number=n))
print("2: format string and args, no output:", timeit(lambda: logger.info("Log: %s: %d", s, i) , number=n))
print("3: formatted string, output", timeit(lambda: logger.error(f"Log: {s}: {i}"), number=n))
print("4: format string and args, output", timeit(lambda: logger.error("Log: %s: %d", s, i) , number=n))
