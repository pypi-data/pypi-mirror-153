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

from datetime import datetime
from flask import current_app, request
from noclouddotnet.utils import yaml_response, read_file
from noclouddotnet.models import Instance
from noclouddotnet import db, metrics

from stevedore import extension

from . import instance_blueprint

from dynaconf import settings, Validator

extidmgr = extension.ExtensionManager(
    namespace="noclouddotnet.instanceid",
    propagate_map_exceptions=True,
    invoke_on_load=False,
)

# Register validators
settings.validators.register(
    # Ensure some parameters exists (are required)
    Validator('INSTANCEID', is_in=extidmgr.entry_points_names()),
)

@instance_blueprint.route('/meta-data', methods=['GET'])
def meta_data():
    """
    Respond to meta-data request; either returning previously associated record
    or generating a new one.

    :returns: yaml instance/host information
    """
    # hmmm - verify http headers (for via, x-forwarded-for etc)
    current_app.logger.info(str(request.environ.items()))
    iid, hostname = extidmgr[current_app.config.INSTANCEID].plugin(request=request)
    instance = Instance.query.filter_by(id=iid).first()
    if instance is None:
        instance = Instance(id=iid,
                            remote_ip=request.remote_addr,
                            first_contact=datetime.now(),
                            hostname=hostname,
                            type=current_app.config.INSTANCE_TYPE,
                            count=0)
        db.session.add(instance)
        db.session.commit()

    data = {
        'hostname': instance.hostname,
        'instance-id': instance.id,
        'instance-type': instance.type,
        'local-hostname': instance.hostname,
        'public-hostname': hostname,
    }

    return yaml_response(data)



@instance_blueprint.route('/user-data', methods=['GET'])
def user_data():
    """
    User data (scripts).
    
    :returns: gzip/blob of cloud-int formatted user data
    """
    return read_file(current_app.config.USER_DATA)


@instance_blueprint.route('/vendor-data', methods=['GET'])
def vendor_data():
    """
    Vendor data (scripts). 

    :returns: gzip/blob of cloud-int formatted user data
    """
    return read_file(current_app.config.VENDOR_DATA)

@instance_blueprint.route('/phone-home', methods=['GET', 'POST'])
def phone_home():
    """
    A cloud-init phone-home data/save.
    The phone-home url should be /phone-home?instance_id=$INSTANCE_ID
    Note that a phone-home call only happens once per cloud-instance.

    :returns: http return code
    """
    form = dict(list(request.form.items()) + list(request.args.items()))
    if not form.get('instance_id', None):
        current_app.logger.error('phone-home: no instance_id from %s' % request.remote_addr)
        return yaml_response({'message': 'no instance_id'}, 400)

    instance = Instance.query.filter_by(id=form['instance_id']).first()
    now = datetime.now()
    # hmmm - this shouldn't happen ...
    if instance is None:
        iid, hostname = extidmgr[current_app.config.INSTANCEID].plugin(request=request)
        instance = Instance(id=iid,
                            remote_ip=request.remote_addr,
                            first_contact = now,
                            type = current_app.config.INSTANCE_TYPE,
                            count = 0)
    data = {
        'hostname': form.get('hostname',''),
        'fqdn': form.get('fqdn',''),
        'remote_ip': request.remote_addr,
        'last_contact': now,
        'pub_key_dsa': form.get('pub_key_dsa',''),
        'pub_key_rsa': form.get('pub_key_rsa',''),
        'pub_key_ecdsa': form.get('pub_key_ecdsa',''),
        'pub_key_ed25519': form.get('pub_key_ed25519',''),
        'count': instance.count + 1
    }
    
    for k,v in data.items():
        setattr(instance, k, v)
        
    db.session.commit()
    return yaml_response('')

@instance_blueprint.route('/fetch', methods=['GET', 'POST'])
def fetch():
    """
    Return all registered instance records.

    :returns: yaml instance data responding to query
    """
    form = dict(list(request.form.items()) + list(request.args.items()))
    results = []
    if form.get('instance_id', None):
        for instance in Instance.query.filter_by(id=form.getlist('instance_id')):
            results.append(instance.to_dict())
    if form.get('remote_ip', None):
        for instance in Instance.query.filter_by(remote_ip=form.getlist('remote_ip')):
            results.append(instance.to_dict())
    if not form.get('instance_id', None) and not form.get('remote_ip', None):
        for instance in Instance.query.all():
            results.append(instance.to_dict())

    return yaml_response(results)

@instance_blueprint.route('/debug', methods=['GET'])
@metrics.do_not_track()
def debug():
    """
    Show debug info; from request.

    :returns: yaml of request and application configuration
    """
    results = [
        str(request.environ.items()),
        current_app.config.items()
    ]
    return yaml_response(results)
