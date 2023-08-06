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


from noclouddotnet import db

class Instance(db.Model):
    """A cloud-init machine instance."""

    id = db.Column(db.String(), primary_key=True)
    remote_ip = db.Column(db.String(), index=True, nullable=True)
    hostname = db.Column(db.String(), nullable=True)
    fqdn = db.Column(db.String(), nullable=True)
    type = db.Column(db.String(20), nullable=True)
    pub_key_dsa = db.Column(db.Text(), nullable=True)
    pub_key_rsa = db.Column(db.Text(), nullable=True)
    pub_key_ecdsa = db.Column(db.Text(), nullable=True)
    pub_key_ed25519 = db.Column(db.Text(), nullable=True)
    first_contact = db.Column(db.DateTime, nullable=True)
    last_contact = db.Column(db.DateTime, nullable=True)
    count = db.Column(db.Integer)

    def to_dict(self):
        """
        A dictionary of object details; suitable for JSON/YAML 
        representations.
        """
        #return(dict((col, getattr(self, col)) for col in self.__table__.columns)
        return(dict((col, getattr(self, col)) for col in ('id',
                                                          'remote_ip',
                                                          'hostname',
                                                          'fqdn',
                                                          'type',
                                                          'pub_key_dsa',
                                                          'pub_key_rsa',
                                                          'pub_key_ecdsa',
                                                          'pub_key_ed25519',
                                                          'first_contact',
                                                          'last_contact',
                                                          'count')))
