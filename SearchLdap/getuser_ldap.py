#!/usr/bin/env python
# -*- coding: utf8 -*-
# @Author: Adrien Néel <FullTacos>
# @Date:   24-Oct-2016
# @Email:  aneel@net-online.fr
# @Project: GetUser LDAP
# @Last modified by:   FullTacos
# @Last modified time: 24-Oct-2016

import argparse
import sys
import ldap

parser = argparse.ArgumentParser()
parser.add_argument("servername", type=str, help=" -> serverldap")
parser.add_argument("username", type=str, help=" -> username")
parser.add_argument("password", type=str, help=" -> password")
parser.add_argument("dnbase", type=str, help=" -> dnbase")


args = parser.parse_args()

if __name__ == "__main__":
    print (servername, username, password, dnbase)
    # adjust this to your base dn for searching
    connect = ldap.open('ldap://'+servername+':389')
    try:
        # if authentication successful, get the full user data
        connect.bind_s(username, password)
        r = connect.search_s(dnbase, ldap.SCOPE_SUBTREE, '(|(objectClass=User)(objectClass=Person)(objectClass=inetOrgPerson))', ['cn', 'mail'])
        for dn, entry in r:
            print 'Processing', repr(dn)
        except ldap.LDAPError:
            connect.unbind_s()
            print "authentication error"
