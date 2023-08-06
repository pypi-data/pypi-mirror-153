# -*- coding: ascii -*-
"""
aedir_tool.passwd - Sets the password of the specified aeUser/aeService or aeHost entry
referenced by uid or host attribute
"""

import sys
import getpass

import ldap0
from ldap0 import LDAPError
from ldap0.filter import escape_str as escape_filter_str

import aedir
from aedir import AUTHC_ENTITY_FILTER_TMPL


def main():
    """
    set password for entry referenced by name
    """

    logger = aedir.init_logger(__name__)

    try:
        arg_value = sys.argv[1]
    except IndexError:
        sys.stderr.write('Usage: {} <username|hostname>\n'.format(sys.argv[0]))
        sys.exit(9)

    with aedir.AEDirObject(None) as aedir_conn:

        logger.debug('successfully connected to %r as %r', aedir_conn.uri, aedir_conn.whoami_s())

        try:
            res = aedir_conn.find_unique_entry(
                aedir_conn.search_base,
                scope=ldap0.SCOPE_SUBTREE,
                filterstr=AUTHC_ENTITY_FILTER_TMPL.format(escape_filter_str(arg_value)),
                attrlist=['1.1'],
            )
        except LDAPError as ldap_err:
            logger.error('LDAPError finding entry for %r: %s', arg_value, ldap_err)
            sys.exit(1)

        new_password1 = getpass.getpass(
            'Enter new password for {} (empty generates password): '.format(res.dn_s)
        )

        if new_password1:
            # ask to repeat password input
            new_password2 = getpass.getpass('repeat password: ')
            if new_password1 != new_password2:
                sys.stderr.write('2nd input for new password differs!\n')
                sys.exit(1)
        else:
            # empty password input => generate random password
            new_password2 = None

        try:
            entry_dn, new_pw = aedir_conn.set_password(arg_value, new_password2)
        except LDAPError as ldap_err:
            logger.error('LDAPError setting password: %s', ldap_err)
            sys.exit(1)

        if new_password2 is None:
            sys.stdout.write('Generated password: %s\n' % (new_pw.decode('utf-8')))
        logger.info('Successfully set password of entry %r', entry_dn)

    # end of main()


if __name__ == '__main__':
    main()
