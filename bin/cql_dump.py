#!/usr/bin/env python
"""
cql_dump is a CLI utility for creating full or partial dumps
of cassandra column families (tables), such that the dump is
a sequence of valid CQL 'INSERT' statemets.

Such dump can be restored by piping through cqlsh

This is somewhat similar to the plain SQL output by mysqldump and pg_dump.
"""
import argparse
import logging
import cassandra.cluster
from cassandra.encoder import cql_encode_all_types

def main():
    """CLI entry-point"""
    parser = argparse.ArgumentParser(
        description='Dump cassandra data in cql format.')

    parser.add_argument('keyspace')
    parser.add_argument('column_family')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug output')
    parser.add_argument('-H', '--hosts',
                        help='comma-separated list of hosts in the cluster')
    parser.add_argument('-p', '--port', type=int, default=9042,
                        help='Cassandra CQL native transport port')
    parser.add_argument('-L', '--limit', type=int, default=10000,
                        help='Add a LIMIT to the select query')
    parser.add_argument('-t', '--timeout', type=int, default=10,
                        help='Query timeout in seconds')
    parser.add_argument('-W', '--where', default=None,
                        help='WHERE clause (without the WHERE)')

    args = parser.parse_args()

    logging.getLogger().setLevel(logging.DEBUG if args.debug else logging.INFO)

    session = setup_session(args.hosts, args.port)
    session.row_factory = make_row_factory(args.keyspace, args.column_family)
    session.default_fetch_size = 5
    session.default_timeout = args.timeout
    session.set_keyspace(args.keyspace)

    query = prepare_query(args.column_family, args.where, args.limit)
    logging.debug("Executing query: %s", query)
    output_results(session.execute(query))


def setup_session(csv_hosts, port):
    """Connect to a Cassandra cluster"""
    hosts = [host.strip() for host in csv_hosts.split(',')]
    cluster = cassandra.cluster.Cluster(hosts, port=port)
    session = cluster.connect()

    return session


def make_row_factory(keyspace, column_family):
    """Prepare INSERT statements for each row in the column family"""
    def _factory(colnames, rows):
        columns = ', '.join('"%s"' % col for col in colnames)
        for row in rows:
            values = ', '.join(cql_encode_all_types(val).decode('utf-8') for val in row)
            yield "INSERT INTO %s.%s (%s) VALUES (%s)" % (
                keyspace, column_family, columns, values)
    
    return _factory


def prepare_query(column_family, where_clause, limit):
    """Prepare the CQL query for the column family"""
    query = "SELECT * FROM %s" % column_family
    if where_clause is not None:
        query += " WHERE " + where_clause

    query += " LIMIT %d" % limit

    return query


def output_results(result_rows):
    """Output the results to STDOUT"""
    for row in result_rows:
        print(row + ';')


if __name__ == '__main__':
    main()
