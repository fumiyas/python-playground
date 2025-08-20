import email
import email.utils
from email import policy
from email.header import decode_header, make_header

#hdr_addrs = '''=?utf-9?q?=22Suporte_HelpDesk_=C2=A9_2022=22_=3Ccstr=40cstr=2Eufcg=2Eedu?=@mail.sms.maceio.al.gov.br, =?utf-8?q?=2Ebr=3E?=@mail.sms.maceio.al.gov.br'''
#hdr_addrs = '''"Alice\n (A)" <a@example.org>, (Bob\n b) <bob@example.org>'''
#hdr_addrs = '''=?UTF-8?B?44GC44GE44GG?= <foo@example.com>, bar<bar@example.jp>'''
#hdr_addrs = '''=?UTF-8?B?44GC44GE44GGQGV4YW1wbGUuY29t?= <foo@example.com>, bar<bar@example.jp>'''
hdr_addrs = '''=?UTF-8?B?44GC44GE44GG?= <foo@example.com>'''
hdr_addrs_made = str(make_header(decode_header(hdr_addrs)))

msg_raw = f"To: {hdr_addrs}\nSubject: test\n\nbody"
msg = email.message_from_string(msg_raw)
msg_default = email.message_from_string(msg_raw, policy=policy.default)
msg_smtp = email.message_from_string(msg_raw, policy=policy.SMTP)

print(f"{hdr_addrs=}")
print(f"{email.utils.getaddresses([hdr_addrs], strict=True)=}")
print(f"{email.utils.parseaddr(hdr_addrs)=}")
print()
print(f"{hdr_addrs_made=}")
print(f"{email.utils.getaddresses([hdr_addrs_made], strict=True)=}")
print(f"{email.utils.parseaddr(hdr_addrs_made)=}")
print()

print(f"{type(msg)=}")
print(f"{type(msg.policy)=}")
print(f"{type(msg._headers)=}")
print(f"{msg.policy=}")
print(f"{msg.policy.raise_on_defect=}")
print(f"{msg.policy.max_line_length=}")
print(f"{msg._headers=}")
print(f"{msg['to']=}")
print(f"{type(msg.get_all('to')[0])=}")
print()

print(f"{type(msg_default)=}")
print(f"{type(msg_default.policy)=}")
print(f"{type(msg_default._headers)=}")
print(f"{msg_default.policy=}")
print(f"{msg_default.policy.raise_on_defect=}")
print(f"{msg_default.policy.max_line_length=}")
print(f"{msg_default._headers=}")
print(f"{msg_default['to']=}")
print()

print(f"{type(msg_smtp)=}")
print(f"{type(msg_smtp.policy)=}")
print(f"{type(msg_smtp._headers)=}")
print(f"{msg_smtp.policy=}")
print(f"{msg_smtp.policy.raise_on_defect=}")
print(f"{msg_smtp.policy.max_line_length=}")
print(f"{msg_smtp['to']=}")
print(f"{msg_smtp['to'].addresses=}")
print(f"{msg_smtp._headers=}")
