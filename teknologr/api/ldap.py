import ldap


class LDAPAccountManager:
    def __init__(self, dry_run=False):  # TODO: dry run used?
        # Attempts not connection, simply initializes the object.
        self.ldap = ldap.initialize(env("LDAP_HOST", "ldaps://localhost:636/"))

    def __enter__(self):
        self.ldap.simple_bind_s(
            env("LDAP_ADMIN_BIND_DN", "cn=manager,dc=example,dc=com"),
            env("LDAP_ADMIN_PW", "somepass")
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ldap.unbind_s()

    def add_account(self, member):
        uidnumber = self.get_next_uidnumber()
        userldif = env("")
        self.ldap.add_s(dn, ldif)

    def get_next_uidnumber(self):
        """Returns the next free uidnumber greater than 1000"""

        output = self.ldap.search("uidNumber")
        uidnumbers = [int(line.split(": ")[1]) for line in output.splitlines() if
                      "uidNumber: " in line]
        uidnumbers.sort()

        # Find first free uid over 1000.
        last = 1000
        for uid in uidnumbers:
            if uid > last + 1:
                break
            last = uid
        return last + 1

