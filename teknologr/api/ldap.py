import ldap
import ldap.modlist as modlist
from getenv import env

import codecs
import hashlib
import time


class LDAPAccountManager:
    def __init__(self, dry_run=False):  # TODO: dry run used?
        # Don't require certificates
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        # Attempts not connection, simply initializes the object.
        self.ldap = ldap.initialize(env("LDAP_SERVER_URI"))

    def __enter__(self):
        self.ldap.simple_bind_s(
            env("LDAP_ADMIN_BIND_DN"),
            env("LDAP_ADMIN_PW")
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ldap.unbind_s()

    def add_account(self, member, password):
        dn = env("LDAP_USER_DN_TEMPLATE") % {'user': member.username}

        uidnumber = self.get_next_uidnumber()
        # The password needs to be stored in a different format for samba
        nt_pw = codecs.encode(
                hashlib.new('md4', password.encode('utf-16le')).digest(),
                'hex_codec'
            ).decode('utf-8').upper()
        attrs = {
            'uid': member.username,
            'cn': member.full_preferred_name,
            'homeDirectory': '/rhome/%s' % member.username,
            'uidNumber': uidnumber,
            'mailHost': 'smtp.ayy.fi',
            'gidNumber': 1000,
            'sn': member.surname,
            'givenName': member.preferred_name,
            'loginShell': '/bin/bash',
            'objectClass': 'kerberosSecurityObject',
            'objectClass': 'inetOrgPerson',
            'objectClass': 'posixAccount',
            'objectClass': 'shadowAccount',
            'objectClass': 'inetLocalMailRecipient',
            'objectClass': 'top',
            'objectClass': 'person',
            'objectClass': 'organizationalPerson',
            'objectClass': 'billAccount',
            'krbName': member.username,
            'mail': member.email,
            'userPassword': password,
            'objectClass': 'sambaSamAccount',
            'sambaSID': "S-1-0-0-%s" % str(uidnumber*2+1000),
            'sambaNTPassword': nt_pw,
            'sambaPwdLastSet': int(time.time()),
        }

        ldif = modlist.addModlist(attrs)
        # TODO handle errors
        self.ldap.add_s(dn, ldif)

        # TODO add user to group
        # TODO return something

    def get_next_uidnumber(self):
        """Returns the next free uidnumber greater than 1000"""
        output = self.ldap.search_s(env("LDAP_USER_DN"), ldap.SCOPE_ONELEVEL, attrlist=['uidNumber'])
        uidnumbers = [int(user[1]['uidNumber'][0]) for user in output]
        uidnumbers.sort()

        # Find first free uid over 1000.
        last = 1000
        for uid in uidnumbers:
            if uid > last + 1:
                break
            last = uid
        return last + 1
