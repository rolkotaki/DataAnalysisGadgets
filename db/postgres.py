import pandas as pd
import psycopg2 as ps
from configparser import ConfigParser


# https://www.postgresqltutorial.com/postgresql-python/
# There is a nice example for an iterator function to return query result:
# "Querying data using fetchmany() method" section at: https://www.postgresqltutorial.com/postgresql-python/query/
# It is basically the same that I showed in file_management/read_write_files.py


def create_connection(user='postgres', password='admin', host='127.0.0.1', port='5432', database='dvdrental'):
    conn = ps.connect(user, password, host, port, database)
    return conn


def create_conn_from_config(filename='database.ini', section='postgresql'):
    # Reading the config
    parser = ConfigParser()
    parser.read(filename)
    # Creating a set for the parameters
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    # Creating the connection to Postgres
    conn = ps.connect(**db)
    return conn


def close_connection(conn):
    if conn:
        conn.close()


def main():
    conn = None
    try:
        # conn = create_connection()
        conn = create_conn_from_config()
        cursor = conn.cursor()

        # Querying data into variables
        cursor.execute("""select city_id, city, country_id from city where city_id = 313""")
        london_rec = cursor.fetchone()
        print(london_rec)  # a tuple is returned
        print(london_rec[1])

        cursor.execute("""select city_id, city, country_id from city where city_id = 313""")
        city_id, city, country_id = cursor.fetchone()
        print(city)

        # Simple looping through the records (we could also create an iterator function for that)

        cursor.execute("""select city_id, city, country_id from city""")
        record = cursor.fetchone()
        result_list = []
        while record is not None:           # fetching the records one by one
            result_list.append(record)
            record = cursor.fetchone()
        print(result_list)

        cursor.execute("""select city_id, city, country_id from city""")
        records = cursor.fetchall()         # fetching the records all at once; returns a list of tuples
        for record in records:              # looping through the result list
            pass  # we can do whatever

        # Querying data into pandas dataframe

        cursor.execute("""select city_id, city, country_id from city""")
        cities = cursor.fetchall()  # returns a list of tuples, where each tuple is a record
                                    # fetchmany(n)  --> returns n number of rows
        # print(cities)
        df_cities = pd.DataFrame(cities, columns=['city_id', 'city_name', 'country_id'])  # dataframe from the result
        print(df_cities.head())

        # We can (should ?) use pandas's built-in functionality
        df_cities = pd.read_sql_query("""select city_id, city, country_id from city""",
                                      conn,  # the connection object
                                      params=None,  # we could use these params for the query
                                      index_col=['city_id'],  # setting index column(s)
                                      parse_dates=None,  # to parse date column to dates instead of objects
                                      chunksize=None  # if the result set is big, we can use chunks, as seen before
                                      )
        print(df_cities.head())

        # DML statement

        cursor.execute("""delete from country  where country = 'Empire of NRPS' """)
        print('Deleted {0} record(s)'.format(cursor.rowcount))
        cursor.execute("""insert into country (country) values ('Empire of NRPS')""")
        print('Inserted {0} record(s)'.format(cursor.rowcount))

        statement = """insert into country (country) values (%s) returning country_id"""
        country = 'Kingdom of NRSP'
        cursor.execute(statement, (country, ))
        new_country_id = cursor.fetchone()[0]
        print('Inserted a new country, the new id is:', new_country_id)
        conn.commit()

        # DDL statement

        cursor.execute("""DROP TABLE IF EXISTS parts""")

        cursor.execute(""" CREATE TABLE parts (
                           part_id SERIAL PRIMARY KEY,
                           part_name VARCHAR(255) NOT NULL
                       )
                       """)
        conn.commit()
        print('PARTS table created')

        # Calling stored procedure

        cursor.callproc("film_in_stock", (133, 1))
        result = cursor.fetchone()[0]  # result could be a result set with multiple records also
        print('Procedure result: ', result)

        cursor.close()
    except (Exception, ps.Error) as error:
        print('Error during db operation: ', error)
    finally:
        close_connection(conn)


if __name__ == "__main__":
    main()
