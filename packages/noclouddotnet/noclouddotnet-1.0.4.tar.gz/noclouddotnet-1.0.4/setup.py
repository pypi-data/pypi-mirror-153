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
from setuptools import setup, find_packages

with open('README.md') as fh:
    long_description = fh.read()

with open('VERSION.txt') as fh:
    version = fh.read().strip()

with open('requirements.txt') as fh:
    install_requires = fh.readlines()
    
setup(name='noclouddotnet',
      version=version,
      description='NoCloudNet Datasource/Metadata server for cloud-init',
      long_description=long_description,
      author='Alan Milligan',
      author_email='alan.milligan@last-bastion.net',
      url='http://linux.last-bastion.net',
      license='GPL',
      project_urls={
          'Documentation': 'https://noclouddotnet.readthedocs.io/',
          'Source': 'https://github.com/milligana/noclouddotnet/',
          'Tracker': 'https://github.com/milligana/noclouddotnet/issues',
      },
      classifiers=[
          "Framework :: Flask",
          "Programming Language :: Python :: 3",
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
          "Topic :: System :: Boot :: Init",
          "Topic :: System :: Operating System Kernels :: Linux"
      ],
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      install_requires=install_requires,
      extras_require = {
          # moved to requirements-docs.txt for readthedocs
          #'docs': [
          #    'doc8',
          #    'm2r2',
          #    'sphinx',
          #    'sphinx_git',
          #    'sphinx_rtd_theme',
          #    'sphinxcontrib.programoutput',
          #],
          'jaeger': [
              'Flask-OpenTracing',
              'jaeger-client',
              ],
          'test': [
              'tox',
              'pytest-cov',
              'pytest-flask',
          ],
          'prospector': [
              'prospector[with_everything]',
          ]
      },
      entry_points = {
          "noclouddotnet.instanceid": [
              "simple = noclouddotnet.instance.instanceid:instance_id_hostname_simple",
              "reversedns = noclouddotnet.instance.instanceid:instance_id_hostname",
          ]
      }
)
