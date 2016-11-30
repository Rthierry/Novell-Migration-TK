#!/usr/bin/env python
# -*- coding: utf8 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   04-Oct-2016
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire de lecture ldap
# @Last modified by:   Gandalf
# @Last modified time: 26-Oct-2016
import ldap
import getopt
import sys
reload(sys)
sys.setdefaultencoding("utf8")


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", AssertionError["ifile="])
    except getopt.GetoptError:
        print 'ldapReqADedir.py -s <ldapserver> -b <base> -'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'nss2csv.py -i <inputfile.xml> deux fichiers en sortie _trustee.csv et _quota.csv'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        print 'Le fichier traité est :', inputfile
    return()

# Accept Self-Sign Certificates
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
Server = "ldaps://172.30.254.44"

BaseAD = "dc=netonline,dc=loc"
BaseeDir = "O=stac"
Scope = ldap.SCOPE_SUBTREE
FilterAD = "(&(objectClass=user)(!(objectClass=computer)))"
FiltereDir = "(&(objectClass=user))"
Attrs = ['loginScript']
l = ldap.initialize(Server)
l.protocol_version = 3
l.set_option(ldap.OPT_REFERRALS, 0)
l.simple_bind_s('cn=admin,ou=94,o=stac', 'root_root')

r = l.search_s(BaseeDir, Scope, FiltereDir, Attrs)

for dn in r:
    print 'Processing', repr(dn)

# mod_attrs = [(ldap.MOD_ADD,'loginScript', 'toto' )]
# l.modify_s('cn=testmac,o=stac', (ldap.MOD_ADD,attr,''))
# l.modify_s('cn=testmac,o=stac', mod_attrs)


def GetLdapMod(dn, attr, value):
    mod_attrs = [(ldap.MOD_DELETE, attr, None)]
    l.modify_s(dn, mod_attrs)
    mod_attrs = [(ldap.MOD_ADD, attr, value)]
    l.modify_s(dn, mod_attrs)
    return

if __name__ == "__main__":
    # GetLdapMod('cn=testmac,o=stac', 'loginScript', 'test depuis python')
    GetLdapMod('cn=testmac,o=stac', 'loginScript', 'tutu')
