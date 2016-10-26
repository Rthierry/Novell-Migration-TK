#!/usr/bin/env python
# -*- coding: utf8 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   04-Oct-2016
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire de lecture ldap
# @Last modified by:   Gandalf
# @Last modified time: 26-Oct-2016

import sys, getopt
reload(sys);
sys.setdefaultencoding("utf8")

import ldap
Server = "ldap://172.16.48.220"

BaseAD = "dc=netonline,dc=loc"
BaseeDir = "O=netonline"
Scope = ldap.SCOPE_SUBTREE
FilterAD = "(&(objectClass=user)(!(objectClass=computer)))"
FiltereDir = ""
Attrs = ['SamAccountName','memberOf']

l =ldap.initialize(Server)
l.protocol_version = 3
l.set_option(ldap.OPT_REFERRALS, 0)
l.simple_bind_s('Administrateur@netonline.loc', 'Netonline@26')
r = l.search_s(BaseAD, Scope, FilterAD, Attrs)
for dn in r:
    print 'Processing', repr(dn)
