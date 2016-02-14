# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Part of Zato - Open-source ESB, SOA, REST, APIs and Cloud Integrations in Python
# https://zato.io

from zato.elem import default_ns, xml

def main(n):

    for x in range(n):

        doc = xml()
        doc.ns_map += {'rem':'http://remoting.example.com/'}, default_ns.s12

        header = doc.s12_Envelope.s12_Header

        header.wsa_Action = 'urn:hl7-org:v3:MCCI_IN000002UV01'
        header.wsa_Action._s12_mustUnderstand = '1'
        header.wsa_Action._actor_type = '2'
        header.wsa_MessageID = 'uuid:123'
        header.wsa_ReplyTo.wsa_Address = 'http://www.w3.org/2005/08/addressing/anonymous'

        arg0 = doc.s12_Envelope.s12_Body.rem_usrOrgRoleLogin.arg0
        arg0.user = 'my-user'
        arg0._rem_is_req = 'true'
        arg0.pwd = 'my-password'
        arg0.role = 'my-role'
        arg0.org = 'my-org'

        arg0.rem_access[0] = 'no'
        arg0.rem_access[0]._rem_type = '0'
        arg0.rem_access[0].access = '000'

        arg0.rem_access[1] = 'yes'
        arg0.rem_access[1]._rem_type = '1'
        arg0.rem_access[1].access = '111'

        doc.to_json()

    return doc

if __name__ == '__main__':
    import datetime

    #import cProfile
    #cProfile.run('main(10000)')

    n = 200
    repeats = 40
    items = []

    for x in range(repeats):
        start = datetime.datetime.utcnow()
        doc = main(n)
        elapsed = datetime.datetime.utcnow() - start
        result = 1.0 / elapsed.total_seconds() * n
        items.append(result)
        print('{:.0f} doc/s'.format(result))

    print('Avg of {:.0f} doc/s after {} repeats'.format(sum(items) / repeats, repeats))
