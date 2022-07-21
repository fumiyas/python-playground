#!/usr/bin/env python
##
## Run a command with a timeout checking
## Copyright (c) 2006-2010 SATOH Fumiyasu @ OSS Technology Corp.
##               <http://www.osstech.co.jp/>
##
## Date: 2010-06-22, since 2006-12-31
## License: GNU General Public License version 2

import getopt
import signal
import re
import sys
import os
import select

def perr(format, *argv):
    print >>sys.stderr, sys.argv[0] + ":", format % argv

timespec_modifiers = {
    'm':	60,
    'h':	60 * 60,
    'd':	60 * 60 * 24,
}

def timespec_to_sec(timespec):
    m = re.match(r'^(\d+)(\w)?$', timespec)
    if not m:
	perr('Invalid time spec: %s' % timespec)
	sys.exit(code_on_usage_error)
    sec = float(m.group(1))
    if m.group(2):
	try:
	    sec *= timespec_modifiers[m.group(2)]
	except KeyError:
	    perr('Invalid time spec: %s' % timespec)
	    sys.exit(code_on_usage_error)
    return sec

signum_by_name = {}
signame_by_num = {}
for signame in dir(signal):
    if signame.startswith("SIG"):
	signum = getattr(signal, signame)
	if type(signum) == type(1):
	    signum_by_name[str(signum)] = signum
	    signum_by_name[signame] = signum
	    signum_by_name[re.sub("^SIG", "", signame)] = signum
	    signame_by_num[signum] = signame

## Options
## ======================================================================

warn_on_timeout = False
signum_on_timeout = signal.SIGTERM

kill_after = 0

code_on_timeout = 124
code_on_usage_error = 125
code_on_exec_error = 126
code_on_fork_error = 127

usage = """Usage: %(program_name)s [OPTIONS] DURATION COMMAND [ARG ...]

Options:
 -s, --signal SIGNAL
    Send SIGNAL to COMMAND on timeout (default: %(signame_on_timeout)s)
 -k, --kill-after DURATION
    Send SIGNAL to COMMAND on timeout (NOT IMPLEMENTED YET!)
 --warn-on-timeout
    Print error message to standard error on timeout
 --timeout-code=EXITCODE
    Exit code on timeout (default: %(code_on_timeout)d)
 --exec-error-code=EXITCODE
    Exit code on exec failure (default: %(code_on_exec_error)d)
 --fork-error-code=EXITCODE
    Exit code on fork failure (default: %(code_on_fork_error)d)
""" % {
    'program_name':		sys.argv[0],
    'signame_on_timeout':	signame_by_num[signum_on_timeout],
    'code_on_timeout':		code_on_timeout,
    'code_on_exec_error':	code_on_exec_error,
    'code_on_fork_error':	code_on_fork_error,
}

## Command-line options
## ----------------------------------------------------------------------

try:
    opts, args = getopt.getopt(sys.argv[1:],
	'hs:s:',
	[
	    'help',
	    'signal=',
	    'kill-after=',
	    'warn-on-timeout',
	    'timeout-code=',
	    'exec-error-code=',
	    'fork-error-code=',
	])
except getopt.error, msg:
    perr("%s", msg)
    sys.exit(code_on_usage_error)
for opt, arg in opts:
    if opt in ('-h', '--help'):
	print usage
	sys.exit(0)
    if opt in ('-s', '--signal'):
	signame = arg.upper()
	if not signum_by_name.has_key(signame):
	    perr("Invalid signal name: %s", signame)
	    sys.exit(code_on_usage_error)
	signum_on_timeout = signum_by_name[signame]
    if opt in ('-k', '--kill-after'):
	kill_after = timespec_to_sec(arg)
    if opt in ('--warn-on-timeout'):
	warn_on_timeout = True
    if opt in ('--timeout-code'):
	code_on_timeout = int(arg)
    if opt in ('--exec-error-code'):
	code_on_exec_error = int(arg)
    if opt in ('--fork-error-code'):
	code_on_fork_error = int(arg)

timeout = timespec_to_sec(args[0])
command = args[1:]

## Main
## ======================================================================

r, w = os.pipe()

try:
    pid = os.fork()
except OSError, e:
    perr("fork failed: %s", e.strerror)
    sys.exit(code_on_fork_error)

## Child process
## ----------------------------------------------------------------------

if pid == 0:
    os.close(r)
    try:
	os.execvp(command[0], command)
    except OSError, e:
	perr("exec failed: %s: %s", command[0], e.strerror)
	sys.exit(code_on_exec_error)

## Parent process
## ----------------------------------------------------------------------

os.close(w)
p = select.poll()
p.register(r, select.POLLIN)
ready = p.poll(timeout * 1000)
if len(ready) == 0:
    if warn_on_timeout:
	perr("Command timed out: %s", command[0])
    os.kill(pid, signum_on_timeout)
    ## FIXME: Implement --kill-after option
    pid_exited, status = os.waitpid(pid, 0)
    sys.exit(code_on_timeout)

pid_exited, status = os.waitpid(pid, 0)
sys.exit(status >> 8)

