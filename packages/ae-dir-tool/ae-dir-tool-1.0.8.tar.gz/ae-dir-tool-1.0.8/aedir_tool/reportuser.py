# -*- coding: ascii -*-
"""
aedir_tool.reportuser - Generates a report of active aeUser entries and their aePerson attributes
"""

import sys
import csv

import ldap0

import aedir

from .reportperson import AEPERSON_ATTRS

AEUSER_ATTRS = [
    'aePerson',
    'uid',
    'uidNumber',
    'entryUUID',
    'aeStatus',
    'aeTicketId',
    'description',
    'memberOf',
    'aeNotBefore',
    'aeNotAfter',
    'pwdChangedTime',
    'createTimestamp',
    'modifyTimestamp',
    'oathHOTPToken',
]

VIRTUAL_ATTRS = [
    'aeZoneName',
]


def main():

    try:
        aeuser_filter = sys.argv[1]
    except IndexError:
        aeuser_filter = '(aeStatus=0)'

    with aedir.AEDirObject(None, cache_ttl=1800.0) as ldap_conn:

        aedir_search_base = ldap_conn.search_base

        msg_id = ldap_conn.search(
            aedir_search_base,
            ldap0.SCOPE_SUBTREE,
            '(&(objectClass=aeUser){0})'.format(aeuser_filter),
            attrlist=AEUSER_ATTRS,
        )

        column_attrs = AEUSER_ATTRS + AEPERSON_ATTRS + VIRTUAL_ATTRS

        csv_writer = csv.DictWriter(sys.stdout, column_attrs, dialect='excel')

        # write first row with attribute names as column names
        csv_writer.writerow({
            at: at
            for at in column_attrs
        })

        for res in ldap_conn.results(msg_id):
            for result in res.rdata:
                user_dn = result.dn_s
                user_entry = result.entry_s
                user_entry['aeZoneName'] = [
                    aedir.extract_zone(user_dn, aeroot_dn=aedir_search_base)
                ]
                # merge referenced aePerson entry into user entry dict
                person_result = ldap_conn.read_s(user_entry['aePerson'][0], attrlist=AEPERSON_ATTRS)
                user_entry.update(person_result.entry_s)
                # merge multiple values into one string
                user_dict = {
                    at: '|'.join(av)
                    for at, av in user_entry.items()
                }
                # write the CSV row to output file
                csv_writer.writerow(user_dict)

    # end of main()


if __name__ == '__main__':
    main()
