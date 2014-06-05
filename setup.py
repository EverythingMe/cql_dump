from setuptools import setup, find_packages
setup(
    name = 'cql_dump',
    version = '0.1b',
    install_requires = ['cassandra-driver>=2.0.1'],
    scripts = ['bin/cql_dump.py'],
    description = 'A CLI utility for creating dumps of cassandra databases',
    url = 'https://github.com/EverythingMe/cql_dump',
    download_url = 'https://github.com/EverythingMe/cql_dump/tarball/0.1',
    author = 'Timor Raiman',
    author_email = 'timor@everything.me'
)
