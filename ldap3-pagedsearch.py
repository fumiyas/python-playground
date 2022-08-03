#!/usr/bin/env python3
## -*- encoding: utf-8 -*- vim:shiftwidth=4

import logging
import sys
import re
import ldap3

logger = logging.getLogger(__name__)

ds_uri = 'ldapi:///var/run/ldapi'
search_base = 'ou=Users,dc=example,dc=co,dc=jp'
search_filter = '(objectClass=person)'
search_attrs = ['*']
search_paged_size = 10000
pw_hash_scheme = ldap3.utils.hashed.HASHED_SHA


def read_passwords_file(pws_file):
    pws_by_uid = {}
    with open(pws_file, 'r', encoding="UTF-8") as f:
        for num, line in enumerate(f, 1):
            ## NOTE: Adhoc CSV parser
            m = re.match(r'^"(?P<uid>[^"]+)","(?P<pw>.*)"$', line)
            if not m:
                logger.error("Invalid CSV line:%s:%d: %s" % (pws_file, num, line))
                continue
            pws_by_uid[m.group('uid')] = re.sub(r'""', '"', m.group('pw'))
    return pws_by_uid


def read_uids_file(uids_file):
    uids = []
    with open(uids_file, 'r', encoding="UTF-8") as f:
        for num, line in enumerate(f, 1):
            line = line.rstrip('\n')
            if not re.match(r'^[a-z]\w+$', line):
                logger.error("Invalid user line:%s:%d: %s" % (uids_file, num, line))
                continue
            uids.append(line)
    return uids


def main(argv):
    pws_by_uid = read_passwords_file(argv.pop(0)) if len(argv) else {}
    uids = read_uids_file(argv.pop(0)) if len(argv) else []

    ds_s = ldap3.Server(ds_uri)
    ds_c = ldap3.Connection(
        ds_s,
        raise_exceptions=True,
        auto_bind=True,
        authentication=ldap3.SASL,
        sasl_mechanism='EXTERNAL',
        sasl_credentials=(),
    )

    cookie = None
    while cookie != b'':
        ds_c.search(
            search_base,
            search_filter,
            attributes=search_attrs,
            paged_size=search_paged_size,
            paged_cookie=cookie
        )
        ## 1.2.840.113556.1.4.319 - LDAP Simple Paged Results - Control - RFC2696
        cookie = ds_c.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']

        for entry in ds_c.entries:
            m = re.match(r'^(?P<attr>[^=]+)=(?P<uid>[^,]+)', entry.entry_dn)
            rdn_attr = m.group('attr')
            rdn_uid = m.group('uid')

            if len(uids) and rdn_uid not in uids:
                continue

            entry_ldif = entry.entry_to_ldif()
            ## Unwrap lines
            entry_ldif = re.sub(r'\n ', '', entry_ldif)
            ## Remove 'version: 1' and comments
            entry_ldif = re.sub(r'^(#|version:).*(\n|$)', '', entry_ldif, flags=re.MULTILINE)
            ## Remove some pwd*
            entry_ldif = re.sub(r'^pwd(FailureTime|AccountLockedTime|History):.*\n', '', entry_ldif, flags=re.MULTILINE)

            if re.match(r'^(cn|uid)$', rdn_attr) and rdn_uid in pws_by_uid:
                hashed = ldap3.utils.hashed.hashed(pw_hash_scheme, pws_by_uid[rdn_uid])
                entry_ldif = re.sub(r'^(userPassword:).*', r'\1 ' + hashed, entry_ldif, flags=re.MULTILINE, count=1)

            print(entry_ldif, end='')


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logformatter = logging.Formatter('%(filename)s: %(levelname)s: %(message)s')
    loghandler = logging.StreamHandler()
    loghandler.setFormatter(logformatter)
    logger.addHandler(loghandler)

    ldap3.utils.log.set_library_log_detail_level(ldap3.utils.log.EXTENDED)

    main(sys.argv[1:])
