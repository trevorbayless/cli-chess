# Copyright (C) 2021-2022 Trevor Bayless <trevorbayless1@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup
from re import findall

metadata_file = open("src/cli_chess/__metadata__.py").read()
metadata = dict(findall(r'__(\w*)__\s*=\s*"([^"]+)"', metadata_file))

requirements = [
    "chess>=1.9.4",
    "berserk-downstream>=0.11.12",
    "prompt-toolkit>=3.0.36"
]

dev_requirements = {
    'dev': [
        'pytest>=7.2.1',
        'pytest-cov>=4.0.0',
        'flake8>=6.0.0'
    ]
}

setup(
    name=metadata['name'],
    version=metadata['version'],
    description=metadata['description'],
    author=metadata['author'],
    author_email=metadata['author_email'],
    url=metadata['url'],
    license=metadata['license'],
    install_requires=requirements,
    setup_requires=requirements,
    extras_require=dev_requirements
)
