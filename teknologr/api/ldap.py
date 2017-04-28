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
        # TODO exception if no username?
        dn = env("LDAP_USER_DN_TEMPLATE") % {'user': member.username}

        uidnumber = self.get_next_uidnumber()
        # The password needs to be stored in a different format for samba
        nt_pw = codecs.encode(
                hashlib.new('md4', password.encode('utf-16le')).digest(),
                'hex_codec'
            ).decode('utf-8').upper()
        # Everything has to be byte string because why the fuck not?
        attrs = {}
        attrs['uid'] = [member.username.encode('utf-8')]
        attrs['cn'] = [member.full_preferred_name.encode('utf-8')]
        homedir = '/rhome/%s' % member.username
        attrs['homeDirectory'] = [homedir.encode('utf-8')]
        attrs['uidNumber'] = [str(uidnumber).encode('utf-8')]
        attrs['mailHost'] = [b'smtp.ayy.fi']
        attrs['gidNumber'] = [b'1000']
        attrs['sn'] = [member.surname.encode('utf-8')]
        attrs['givenName'] = [member.preferred_name.encode('utf-8')]
        attrs['loginShell'] = [b'/bin/bash']
        attrs['objectClass'] = [
            b'kerberosSecurityObject',
            b'inetOrgPerson',
            b'posixAccount',
            b'shadowAccount',
            b'inetLocalMailRecipient',
            b'top',
            b'person',
            b'organizationalPerson',
            b'billAccount',
            b'sambaSamAccount'
        ]
        attrs['krbName'] = [member.username.encode('utf-8')]
        attrs['mail'] = [member.email.encode('utf-8')]
        attrs['userPassword'] = [password.encode('utf-8')]
        sambasid = "S-1-0-0-%s" % str(uidnumber*2+1000)
        attrs['sambaSID'] = [sambasid.encode('utf-8')]
        attrs['sambaNTPassword'] = [nt_pw.encode('utf-8')]
        attrs['sambaPwdLastSet'] = [str(int(time.time())).encode('utf-8')]

        ldif = modlist.addModlist(attrs)
        # TODO handle errors, what if account exists?
        try:
            self.ldap.add_s(dn, ldif)
        except ldap.ALREADY_EXISTS as e:
            return "fail"

        return "success"

        # TODO add user to group
        # TODO password set workaround?
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
