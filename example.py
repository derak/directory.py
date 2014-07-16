#!/usr/bin/python
#
# Example of how to add a user to Active Directory using,
# LDAP Directory management, wrapper for python-ldap (http://www.python-ldap.org)
#
#
# Derak Berreyesa
# github.com/derak
#####################################################################

import sys, json
import ldap
import ldap.modlist as modlist

import directory

result = {}

firstname   = 'Joe'
lastname    = 'Blow'
username    = 'jblow'
password    = 'some_secret_password'

email = username + '@mycompany.com'
displayName = '%s %s' % (firstname, lastname)

# The dn of our new entry/object
dn="cn=%s,%s" % (displayName, 'ou=Users,dc=ad,dc=mycompany,dc=com')

# A dict to help build the "body" of the object
attrs = {}
attrs['objectclass'] = ['top','person','organizationalPerson','user']
attrs['cn'] = str(displayName)
attrs['sAMAccountname'] = str(username)
attrs['userPassword'] = str(password)
attrs['givenName'] = str(firstname)
attrs['sn'] = str(lastname)
attrs['displayName'] = str(displayName)
attrs['userPrincipalName'] = "%s@ad.mycompany.com" % username
attrs['mail'] = str(email)

# Some flags for userAccountControl property
SCRIPT                    = 1
ACCOUNTDISABLE            = 2
HOMEDIR_REQUIRED          = 8
PASSWD_NOTREQD            = 32
NORMAL_ACCOUNT            = 512
DONT_EXPIRE_PASSWORD      = 65536
TRUSTED_FOR_DELEGATION    = 524288
PASSWORD_EXPIRED          = 8388608

# userAccountControl can be edited later by calling the user_mod method,
# but it is needed for creating an account

# this works!
attrs['userAccountControl'] = str(NORMAL_ACCOUNT + ACCOUNTDISABLE + DONT_EXPIRE_PASSWORD)

## this works w/o secure
##attrs['userAccountControl'] = str(PASSWD_NOTREQD + NORMAL_ACCOUNT + DONT_EXPIRE_PASSWORD)

## this does not work :-(
##attrs['userAccountControl'] = str(NORMAL_ACCOUNT + DONT_EXPIRE_PASSWORD)


# put all of your group dn's into a list to pass to add_user_to_groups()
group_dn_list = ['cn=Engineers,ou=Groups,dc=ad,dc=mycompnay,dc=com',
                 'cn=Interns,ou=Groups,dc=ad,dc=mycompnay,dc=com',
                 'cn=ProjectManagers,ou=Groups,dc=ad,dc=mycompnay,dc=com',
                 'cn=Executives,ou=Groups,dc=ad,dc=mycompnay,dc=com'
                ]

# create a Directory instance and start doing work 
d = directory.Directory();
d.connect('ldaps://ad.mycompnay.com', 'AD\admin_user', password)
d.add_user(dn, attrs)
d.add_user_to_groups(dn, group_dn_list)
d.set_password(dn, password)
d.enable_user(dn, NORMAL_ACCOUNT + DONT_EXPIRE_PASSWORD)
d.disconnect()

result = d.get_result()
result['status'] = 'Success!'

# send result to stdout (or to PHP)
print json.dumps(result)

