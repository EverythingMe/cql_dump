from setuptools import setup, find_packages
setup(
    name = 'cql_dump',
    version = '0.1',
    install_requires = ['cassandra-driver>=2.0.1'],
    packages = ['cql_dump'],
    description = 'A CLI utility for creating dumps of cassandra databases',
    url = 'https://github.com/EverythingMe/cql_dump',
    author = 'Timor Raiman',
    author_email = 'timor@everything.me'
)
