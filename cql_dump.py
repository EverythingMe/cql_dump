#!/usr/bin/env python

import argparse
import logging
import cassandra.cluster

def main():
    parser = argparse.ArgumentParser(description='Dump cassandra data in cql format.')
    parser.add_argument('keyspace')
    parser.add_argument('column_family')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    

    session = setup_session(args)

    session.set_keyspace(args.keyspace)

    rows = session.execute('SELECT * FROM %s', (args.column_family))

    print rows





def setup_session(args):
    cluster = cassandra.cluster.Cluster(['54.85.130.35'], port=9160)
    session = cluster.connect()
    
    return session



if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
