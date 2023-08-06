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

import pytest
from flask import url_for

from noclouddotnet.instance.routes import extidmgr

#@pytest.mark.usefixtures('client_class')
#class TestSuite:
#  
#  def test_01_meta_data(self):
#    #response = self.client.get(url_for('/meta-data'))
#    response = self.client.get('/meta-data')
#    assert response.status_code == 200

def test_00_extensions():
    assert extidmgr.entry_points_names() == ['reversedns', 'simple']
    assert extidmgr.names() == ['reversedns', 'simple']
    
def test_01_extension_simple():
    simple = extidmgr['simple'].plugin
    # cannot test this without an app context ...

def test_02_user_data(test_client):
    response = test_client.get('/user-data')
    assert response.status_code == 200
    assert response.text == ''

# hmmm - non-fixture test ...
def test_03_meta_data(test_client, init_database):
    response = test_client.get('/meta-data')
    assert response.status_code == 200
  
