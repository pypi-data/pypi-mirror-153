#    Copyright 2022 @jack-tee
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

exec(open('faux_data/version.py').read())

LONG_DESCRIPTION = """\
# Faux Data

Faux Data is a library for generating data using configuration files.

See the project on github for more info - https://github.com/jack-tee/faux-data

"""

setup(name='faux-data',
      version=__version__,
      description='Generate fake data from yaml templates',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      author='jack-tee',
      author_email='10283360+jack-tee@users.noreply.github.com',
      packages=['faux_data'],
      include_package_data=True,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.10",
          "License :: OSI Approved :: Apache Software License",
      ],
      install_requires=[
          "pandas==1.4.2",
          "google-cloud-bigquery",
          "google-cloud-pubsub",
          "pyarrow",
          "pyyaml",
          "jinja2",
          "tabulate",
          "fsspec",
          "gcsfs",
      ],
      entry_points={'console_scripts': ['faux=faux_data.cmd:main']})
