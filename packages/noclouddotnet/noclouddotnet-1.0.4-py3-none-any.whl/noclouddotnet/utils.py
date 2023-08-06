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


import os
from flask import make_response
from functools import lru_cache
import yaml


def yaml_response(output, return_code=200):
    """Create a HTTP Response with yamlified output.

    :param output: a python type
    :param return_code: a HTTP return code
    :returns: a Flask HTTP/Response
    """
    resp = make_response(yaml.dump(output), return_code)
    resp.headers['Content-Type'] = 'text/yaml; charset=ascii'
    return resp


@lru_cache(maxsize=None)
def read_file(fpath):
    """Return content of file - see cloud-init user file creation for how to create payloads.

    :param fpath: path to a file on the server host
    :returns: the (cached) content of the file
    """
    if fpath and os.path.exists(fpath):
        with open(fpath, 'rb') as fh:
            return fh.read()
    return ''

