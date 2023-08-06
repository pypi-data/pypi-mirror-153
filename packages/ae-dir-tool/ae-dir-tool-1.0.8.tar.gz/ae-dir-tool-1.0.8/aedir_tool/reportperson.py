# -*- coding: ascii -*-
"""
aedir_tool.reportperson - Generates a report of aePerson entries referenced by active aeUser entries
"""

import sys
import csv

import ldap0
from ldap0.controls.deref import DereferenceControl

import aedir

AEUSER_ATTRS = ['uid']

AETOKEN_ATTRS = ['aeOwner', 'serialNumber']

AEPERSON_ATTRS = [
    'sn',
    'givenName',
    'cn',
    'mail',
    'uniqueIdentifier',
    'aeStatus',
    'employeeNumber',
    'employeeType',
    'telephoneNumber',
    'mobile',
    'homePhone',
    'aeDept',
    'ou',
    'departmentNumber',
    'o',
    'street',
    'l',
    'c',
]

# dereference the AEPERSON_ATTRS from the aeUser entry via attribute aePerson
DEREF_CONTROL = DereferenceControl(True, {'aePerson': AEPERSON_ATTRS})


def main():

    try:
        aeuser_filter = sys.argv[1]
    except IndexError:
        aeuser_filter = '(aeStatus=0)'

    person_dict = {}

    with aedir.AEDirObject(None, cache_ttl=1800.0) as ldap_conn:

        msg_id = ldap_conn.search(
            ldap_conn.search_base,
            ldap0.SCOPE_SUBTREE,
            '(&(objectClass=aeUser){0})'.format(aeuser_filter),
            attrlist=AEUSER_ATTRS,
            req_ctrls=[DEREF_CONTROL],
        )

        for res in ldap_conn.results(msg_id):
            for result in res.rdata:
                # process dn and entry
                if result.ctrls and result.ctrls[0].controlType == DereferenceControl.controlType:
                    deref_control = result.ctrls[0]
                    aeperson_key = deref_control.derefRes['aePerson'][0].dn_s.lower()
                    if aeperson_key in person_dict:
                        for at in AEUSER_ATTRS:
                            if at in result.entry_s:
                                person_dict[aeperson_key][at].update(result.entry_s[at])
                    else:
                        person_dict[aeperson_key] = dict([
                            (at, '|'.join(av))
                            for at, av in deref_control.derefRes['aePerson'][0].entry_s.items()
                        ])
                        for at in AEUSER_ATTRS:
                            person_dict[aeperson_key][at] = set(result.entry_s.get(at, []))

        msg_id = ldap_conn.search(
            ldap_conn.search_base,
            ldap0.SCOPE_SUBTREE,
            '(&(objectClass=aeDevice)(objectClass=oathToken)(aeOwner=*))',
            attrlist=AETOKEN_ATTRS,
        )

        for res in ldap_conn.results(msg_id):
            for result in res.rdata:
                aeperson_key = result.entry_s['aeOwner'][0].lower()
                if aeperson_key in person_dict:
                    tokens = person_dict[aeperson_key].get('oathToken', [])
                    tokens.extend(result.entry_s['serialNumber'])
                    person_dict[aeperson_key]['oathToken'] = tokens

    # convert multi-valued lists in single string
    for pkey in person_dict.keys():
        for at in AEUSER_ATTRS+['oathToken']:
            if at in person_dict[pkey]:
                person_dict[pkey][at] = '|'.join(person_dict[pkey][at])

    # write first row with attribute names as column names
    csv_writer = csv.DictWriter(
        sys.stdout,
        AEPERSON_ATTRS+AEUSER_ATTRS+['oathToken'],
        dialect='excel'
    )
    csv_writer.writerow(
        dict([
            (at, at)
            for at in AEPERSON_ATTRS+AEUSER_ATTRS+['oathToken']
        ])
    )
    csv_writer.writerows(person_dict.values())

    # end of main()


if __name__ == '__main__':
    main()
