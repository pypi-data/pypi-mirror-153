# -*- coding: ascii -*-
"""
aedir_tool.addzone - Add a zone with two role groups for zone admins / auditors and an init tag
"""

import sys

import aedir


def main():
    """
    add the zone with parameters from command-line
    """
    logger = aedir.init_logger(__name__)
    try:
        zone_cn, ticket_id, zone_desc = sys.argv[1:]
    except (IndexError, ValueError, UnicodeError):
        logger.error('Missing or wrong command-line args')
        sys.stderr.write(
            '\n\nUsage: {} <zone name> <ticket ID> <description>\n'.format(
                sys.argv[0]
            )
        )
        sys.exit(9)
    with aedir.AEDirObject(None) as aedir_conn:
        zone_dn = aedir_conn.add_aezone(zone_cn, ticket_id, zone_desc)
    logger.info('Added zone entry %r', zone_dn)


if __name__ == '__main__':
    main()
