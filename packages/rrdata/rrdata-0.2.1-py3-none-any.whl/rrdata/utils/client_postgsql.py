#!/usr/bin/python
import psycopg2
from rrdata.utils.config_postgresql import database_uri, get_config_ini

def connect_postgrsql():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = database_uri
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        print(conn)
        # create a cursor
        cur = conn.cursor()
    	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def client_pgsql(db_name="rrdata"):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        section_name = f"pgsql_{db_name}"
        params = get_config_ini(filename='config.ini', section=section_name)
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        print(conn)
        # create a cursor
        cur = conn.cursor()
    	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect_postgrsql()
    client_pgsql()