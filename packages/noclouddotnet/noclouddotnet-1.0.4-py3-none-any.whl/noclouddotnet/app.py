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
command line interface for NoCloud.Net

currently used to create/migrate RDBMS
"""

from noclouddotnet import create_app, db
from noclouddotnet.models import Instance

import click
from flask.cli import AppGroup, with_appcontext
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)


# set up db/migrations etc
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, instance=Instance)

#db_cli = App.group('db')
@click.command('createdb')
@with_appcontext
def create_db():
    """Create application database/tables."""
    db.create_all()

app.cli.add_command(create_db)


if __name__ == '__main__':
    app.run()

