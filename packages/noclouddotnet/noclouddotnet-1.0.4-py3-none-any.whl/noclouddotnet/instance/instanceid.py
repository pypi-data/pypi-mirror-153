#
#  This file is part of NoCloud.Net.
#
#  Copyright (C) 2022 Last Bastion Network Pty Ltd
#
#  NoCloud.Net is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later version.
#
#  NoCloud.Net is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
#  PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  NoCloud.Net. If not, see <https://www.gnu.org/licenses/>. 
#

__doc__ = """
 bunch of functors to return instanceid, hostname for /meta-data call
 these are invoked using stevedore setuptools/entry points
"""

from flask import current_app

import dns.reversename
import dns.resolver
import uuid

from noclouddotnet.models import Instance

resolver = dns.resolver.Resolver()

def instance_id_hostname(request=None):
    """
    Make an instance-id based upon reverse lookup of remote address.

    :param request: flask request object
    :returns: instance id, hostname tuple
    """
    # TODO - domain from config vs remote_ip
    hostname = 'A'
    domain = current_app.config.DOMAIN
    if request:
        instance = Instance.query.filter_by(remote_ip=request.remote_addr).first()
        if instance:
            return instance.id, instance.hostname

        answers = resolver.resolve_address(request.remote_addr)
  
        if answers:
            hostname = answers[0].to_text().split('.')[0]
            domain  = '.'.join(answers[0].to_text().split('.')[1:])
            if len(domain) and domain[-1] == '.':
                domain = domain[:-1]

    iid = '%s-%s' % (hostname, uuid.uuid4().hex[-12:])
    if domain:
        return iid, "%s.%s" % (hostname, domain)
    return iid, hostname


def instance_id_hostname_simple(request=None):
    """
    Return a uuid-based hostname.

    :param request: flask request object
    :returns: instance id, hostname tuple
    """
    iid = 'A-%s' % uuid.uuid4().hex[-12:]
    domain = current_app.config.DOMAIN

    if domain:
        return iid, "%s.%s" % (iid, domain)
 
    return iid, iid
