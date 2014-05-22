cql_dump
========

Extract a CQL dump from cassandra

Intro
-----
`cql_dump` is a CLI utility for creating full or partial dumps
of cassandra column families (tables), such that the dump is
a sequence of valid CQL 'INSERT' statements, and hence can be
restored by piping through cqlsh (like the output of pg_dump can be
piped through psql)

Usecases:
* migrating data to clusters of different geometry
* migrating data to a cluster of an incompatitable sstable binary format
* extracting a data subset to be loaded into a mockup environment

Dumping Data:
-------------
Usage:
```cql_dump.py [-h] [-d] [-H HOSTS] [-p PORT]
	   [-L LIMIT] [-t TIMEOUT] [-W WHERE]
       keyspace column_family```
Example:
```cql_dump.py -H my_server.local -L 500 my_keyspace my_column_family > output.cql```

Restoring Data From a Dump
--------------------------
cat output.cql | cqlsh my_new_server.local


Notes
-----
cql_dump was inspired by: https://github.com/data-axle/cassandra_backup


Requirements
-------------
What made this project so simple is the great work behind the python *cassandra-driver* by
*datastax*. We require the betta version to be installed:
```pip install cassandra-driver==2.0.0b1```


Todo
----
* Support cql authentication
* Support very large dumps
