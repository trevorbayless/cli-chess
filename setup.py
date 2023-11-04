# Copyright (C) 2021-2023 Trevor Bayless <trevorbayless1@gmail.com>
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

dependencies = [
    "chess>=1.9.4,<2.0.0",
    "berserk>=0.13.1,<0.14.0",
    "prompt-toolkit==3.0.39"  # pin as breaking changes have been
                              # introduced in previous patch versions
                              # read PT changelog before bumping
]

dev_dependencies = {
    'dev': [
        'pytest>=7.2.1,<8.0.0',
        'pytest-cov>=4.0.0,<5.0.0',
        'pytest-socket>=0.6.0,<1.0.0',
        'flake8>=5.0.4,<7.0.0',
        'vulture>=2.7,<3.0'
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
    install_requires=dependencies,
    setup_requires=dependencies,
    extras_require=dev_dependencies
)
