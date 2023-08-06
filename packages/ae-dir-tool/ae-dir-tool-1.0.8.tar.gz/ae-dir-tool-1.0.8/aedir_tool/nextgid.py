# -*- coding: ascii -*-
"""
aedir_tool.nextgid - Sets next GID number to highest GID found + 1
"""

import sys

import ldap0

import aedir

GID_ATTR = 'gidNumber'

UID_ATTR = 'uidNumber'

UID_GID_ALIGN = True


def main():
    """
    run the script
    """

    logger = aedir.init_logger(__name__)

    with aedir.AEDirObject(None) as aedir_conn:

        highest_gid_number = aedir_conn.find_highest_id(
            id_pool_dn=aedir_conn.search_base,
            id_pool_attr=GID_ATTR,
        )
        aeroot_entry = aedir_conn.read_s(
            aedir_conn.search_base,
            attrlist=[GID_ATTR, UID_ATTR]
        ).entry_s

        try:
            current_next_gid = int(aeroot_entry[GID_ATTR][0])
        except KeyError:
            current_next_gid = None
        logger.debug('Current %r value: %s', GID_ATTR, current_next_gid)
        try:
            current_next_uid = int(aeroot_entry[UID_ATTR][0])
        except KeyError:
            current_next_uid = None
        logger.debug('Current %r value: %s', UID_ATTR, current_next_uid)

        modlist = []

        # first add modifications for next GID attribute
        if current_next_gid != highest_gid_number+1:
            modlist.append(
                (ldap0.MOD_ADD, GID_ATTR.encode('ascii'), [str(highest_gid_number+1).encode('ascii')])
            )
            if current_next_gid is not None:
                modlist.append(
                    (ldap0.MOD_DELETE, GID_ATTR.encode('ascii'), [str(current_next_gid).encode('ascii')])
                )
        else:
            logger.debug('Current %r value %d seems ok => no change.', GID_ATTR, current_next_gid)


        if current_next_uid is not None:

            if UID_GID_ALIGN:
                highest_uid_number = highest_gid_number
            else:
                highest_uid_number = aedir_conn.find_highest_id(
                    id_pool_dn=aedir_conn.search_base,
                    id_pool_attr=UID_ATTR,
                )

            if current_next_uid != highest_uid_number+1:
                modlist.append(
                    (ldap0.MOD_ADD, UID_ATTR, [str(highest_uid_number+1)])
                )
                if current_next_uid is not None:
                    modlist.append(
                        (ldap0.MOD_DELETE, UID_ATTR, [str(current_next_uid)])
                    )
            else:
                logger.debug(
                    'Current %r value %d seems ok => no change.',
                    UID_ATTR,
                    current_next_uid,
                )

        if modlist:
            aedir_conn.modify_s(aedir_conn.search_base, modlist)
            logger.info(
                'Updated entry %r with %r',
                aedir_conn.search_base,
                modlist,
            )
        else:
            logger.info('no modifications')

    # end of main()


if __name__ == '__main__':
    main()
