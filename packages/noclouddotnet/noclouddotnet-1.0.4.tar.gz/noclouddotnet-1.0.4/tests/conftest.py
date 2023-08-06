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
from noclouddotnet import create_app, db
from flask import Response

class NoCloudResponse(Response):
    """ implement custom deserializers ?? """

@pytest.fixture
def app():
    flask_app = create_app()
    flask_app.debug = True
    #flask_app.response_class = NoCloudResponse

    return flask_app



@pytest.fixture(scope='module')
def test_client():
    """ hmmm - a test client ..."""
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!



@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

