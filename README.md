cql_dump
========

cql_dump is a CLI utility for creating dumps cassandra databases, akin to mysqldump and pg_dump.

Intro
-----
cql_dump allows dumping and restoring cassandra data in human-readable cql format, such that a single dump contains a full snapshot of the entire data set.

Additionally, cql_dump allows breaking the data into small chunks along the way and upload piece-wise to S3.

How-to
-------
Dumping a Keyspace:

    cql_dump keyspace_name column_family >latest_dump.cql

Restoring can be done via cqlsh:

    cqlsh <latest_dump.cql

Notes
-----
cql_dump takes its inspiration from Data Axle's cassandra_backup (https://github.com/data-axle/cassandra_backup)