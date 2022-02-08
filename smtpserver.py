#!/usr/bin/env python
## -*- coding: utf-8 -*- vim:shiftwidth=4:expandtab:

from __future__ import print_function

import smtpd
import asyncore

class CustomSMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        print('PEER:', peer)
        print('MAIL FROM:', mailfrom)
        print('RCPT TO:', rcpttos)
        print('DATA:')
        print(data)
        return

server = CustomSMTPServer(('127.0.0.1', 1025), None)

asyncore.loop()
