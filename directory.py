#!/usr/bin/python
#
# LDAP Directory management, wrapper for python-ldap (http://www.python-ldap.org)
# Provides higher level control of LDAP Directory management
#
# Some code was originally taken from samples available here:
# http://www.grotan.com/ldap/python-ldap-samples.html
#
#
# Derak Berreyesa
# github.com/derak
#####################################################################

import sys, json
import ldap
import ldap.modlist as modlist


class Directory(object):

    def __init__(self):
        self.result = {}
        self.l = None

    def connect(self, url, username, password):
        try:
            # Create a new user in Active Directory
            ldap.set_option(ldap.OPT_REFERRALS, 0)

            # Allows us to have a secure connection
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)

            # Open a connection
            self.l = ldap.initialize(url)

            # Bind/authenticate with a user with apropriate rights to add objects
            self.l.simple_bind_s(username, password)
                        
        except ldap.LDAPError, e:
            sys.stderr.write('Error connecting to LDAP server: ' + str(e) + '\n')
            self.result['status'] = 'Error connecting to LDAP server: ' + str(e) + '\n'
            print json.dumps(self.result)
            sys.exit(1)

    def add_user(self, dn, attrs):
        try:
            # Convert our dict to nice syntax for the add-function using modlist-module
            ldif = modlist.addModlist(attrs)

            # Add user
            self.l.add_s(dn,ldif)

        except ldap.LDAPError, e:
            sys.stderr.write('Error with LDAP add_user: ' + str(e) + '\n')
            self.result['status'] = 'Error with LDAP add_user: ' + str(e) + '\n'
            print json.dumps(self.result)
            sys.exit(1)

    def add_user_to_groups(self, dn, group_dn_list):
        try:
            # Add user to groups as member
            mod_attrs = [( ldap.MOD_ADD, 'member', dn )]

            for g in group_dn_list:
                self.l.modify_s(g, mod_attrs)

        except ldap.LDAPError, e:
            sys.stderr.write('Error: adding user to group(s): ' + str(e) + '\n')
            self.result['status'] = 'Error: adding user to group(s): ' + str(e) + '\n'
            print json.dumps(self.result)
            sys.exit(1)


    def set_password(self, dn, password):
        # HERE YOU MAKE THE utf-16-le encode password
        unicode_pass = unicode('\"' + password + '\"', 'iso-8859-1')
        password_value = unicode_pass.encode('utf-16-le')

        # change the atribute in the entry you just created
        add_pass = [(ldap.MOD_REPLACE, 'unicodePwd', [password_value])]

        try:
            self.l.modify_s(dn, add_pass)
        except ldap.LDAPError, error_message:
            self.result['status'] = 'Error: could not change password: ' + str(error_message) + '\n'
            print json.dumps(self.result)
            sys.exit(1)
        else:
            self.result['status'] = 'Successfully changed password \n'


    def modify_user(self, dn, flag):
        """Modify user, flag is userAccountControl property"""
        # 512 will set user account to enabled
        # change the user to enabled
        mod_acct = [(ldap.MOD_REPLACE, 'userAccountControl', str(flag))]

        try:
            self.l.modify_s(dn, mod_acct)
        except ldap.LDAPError, error_message:
            self.result['status'] = 'Error: could not modify user: ' + str(error_message) + '\n'
            print json.dumps(self.result)
            sys.exit(1)
        else:
            self.result['status'] = 'Successfully modified user \n'

    def print_users(self, base_dn, attrs):
        filter = '(objectclass=person)'
        users = self.l.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attrs)
        for row in users:
            print row

    def disconnect(self):
        self.l.unbind_s()

    def get_result(self):
        return self.result


if __name__ == '__main__':
    print 'This is directory.py'

