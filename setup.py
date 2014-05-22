from setuptools import setup, find_packages
setup(
    name = 'cql_dump',
    version = '0.1',
    install_requires = ['cassandra-driver>=2.0.0b1'],
    packages = ['cql_dump'],
    description = 'a CLI utility for creating dumps cassandra databases',
)
