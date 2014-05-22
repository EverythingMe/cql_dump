#!/usr/bin/env python

import argparse
import logging
import cassandra.cluster
from cassandra.encoder import cql_encode_all_types

def main():
    parser = argparse.ArgumentParser(description='Dump cassandra data in cql format.')
    parser.add_argument('keyspace')
    parser.add_argument('column_family')
    parser.add_argument('-d', '--debug',   help='enable debug output', action='store_true')
    parser.add_argument('-H', '--hosts',   help='comma-separated list of hosts in the cluster')
    parser.add_argument('-p', '--port',    help='Cassandra CQL native transport port', default=9042)
    parser.add_argument('-L', '--limit',   help='Add a LIMIT to the select query', type=int, default=10000)
    parser.add_argument('-t', '--timeout', help='Query timeout in seconds', type=int, default=10)
    parser.add_argument('-W', '--where',   help='WHERE clause (without the WHERE)', default=None)



    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    

    session                    = setup_session(args)    
    session.row_factory        = make_row_factory(args.keyspace, args.column_family)
    session.default_fetch_size = 5
    session.default_timeout    = args.timeout
    session.set_keyspace(args.keyspace)

    # Format query..
    query = "SELECT * FROM %s" % (args.column_family,)
    if args.where is not None:
        query = query + " WHERE " + args.where

    query = query + " LIMIT %d" % args.limit
    #

    logging.debug("Executing query: %s", query)
    rows = session.execute(query)

    for r in rows:
        print r+';'


def make_row_factory(keyspace, column_family):
    def _factory(colnames, rows):
        columns = '"'+'", "'.join(colnames)+'"'
        for r in rows:
            r = map(cql_encode_all_types, r)
            values = ', '.join(r)
            yield "INSERT INTO %s.%s (%s) VALUES (%s)" % (keyspace, column_family, columns, values)
    
    return _factory
    


def setup_session(args):
    hosts = map(str.strip, args.hosts.split(','))
    cluster = cassandra.cluster.Cluster(hosts, port=args.port)
    session = cluster.connect()
    
    return session



if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
