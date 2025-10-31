#!/usr/bin/env python3

import email
import email.errors
import email.message
import email.policy
import logging

logger = logging.getLogger(__name__)


class MyPolicy(email.policy.Compat32):
    def handle_defect(self, msg, defect):
        if isinstance(
            defect,
            email.errors.InvalidMultipartContentTransferEncodingDefect
        ) and msg.get('content-transfer-encoding', '').lower() == 'base64':
            logger.warning(
                "Ignore message defect: Message is `Content-Type: multiplart/*`,"
                " but `Content-Transfer-Encoding: base64`"
            )
            return
        super().handle_defeat(msg, defect)


msg_bytes = b"""\
Subject: test invalid email
MIME-Version: 1.0
Content-Type: multipart/alternative; charset="utf8";
 boundary="===============1580574656474728575=="
Content-Transfer-Encoding: base64

--===============1580574656474728575==
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit

Blah...

--===============1580574656474728575==--
"""

msg = email.message_from_bytes(msg_bytes, email.message.Message)
print(msg.policy, msg.defects)

policy = MyPolicy()
msg = email.message_from_bytes(msg_bytes, email.message.Message, policy=policy)
print(msg.policy, msg.defects)
