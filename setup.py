from setuptools import setup
from re import findall

metadata_file = open("src/cli_chess/__metadata__.py").read()
metadata = dict(findall(r'__(\w*)__\s*=\s*"([^"]+)"', metadata_file))

dependencies = [
    "chess>=1.9.4,<2.0.0",
    "berserk>=0.13.1,<0.14.0",
    "prompt-toolkit==3.0.47"  # pin as breaking changes have been
                              # introduced in previous patch versions
                              # read PT changelog before bumping
]

dev_dependencies = {
    'dev': [
        'pytest>=7.2.1,<8.0.0',
        'pytest-cov>=4.0.0,<5.0.0',
        'pytest-socket>=0.6.0,<1.0.0',
        'flake8>=5.0.4,<7.0.0',
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
