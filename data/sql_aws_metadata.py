# %%
import sqlite3 as sql
from utils.logger import Log

class Metadata:

    def __init__(self):
        self.database_name = 'data/metadata_storage.db'
        self.table_name_goes = 'goes_metadata'
        self.table_name_nexrad = 'nexrad_metadata'

        # creating the database
        self.conn = sql.connect(self.database_name)
        self.cursor = self.conn.cursor()

        self.create_table_goes()
        self.create_table_nexrad()

    # def __del__(self):
    #     self.db_conn_close()

    # def create_database(self):
    #     conn = sql.connect(self.database_name)
    #     cursor = conn.cursor()
    #     return conn, cursor

    def create_table_goes(self):
        # create sql lite 3 database
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS '''+ self.table_name_goes + ''' (
                station VARCHAR NOT NULL,
                year INTEGER NOT NULL,
                day INTEGER NOT NULL,
                hour INTEGER NOT NULL
                ); ''')

    def create_table_nexrad(self):
        # create sql lite 3 database
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS '''+ self.table_name_nexrad + ''' (
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                day_of_year INTEGER NOT NULL,
                station_id INTEGER NOT NULL
                ); ''')

    def db_conn_close(self):
        self.conn.commit()
        Log().i('Data entered successfully.')
        self.conn.close()
        if (self.conn):
            self.conn.close()
            Log().i("The SQLite connection is closed.")

    def insert_data_into_goes(self, station, year, day, hour):
        insert_str = f'INSERT INTO "{self.table_name_goes}" VALUES("{station}", "{year}", "{day}", "{hour}");'
        self.cursor.execute(insert_str)
        self.db_conn_close()


    def insert_data_into_nexrad(self, year, month, day_of_year, station_id):
        insert_str = f'INSERT INTO "{self.table_name_nexrad}" VALUES("{year}", "{month}", "{day_of_year}", "{station_id}");'
        self.cursor.execute(insert_str)
        self.db_conn_close()

    def print_and_validate_data(self, table_name):
        self.cursor.execute("SELECT * FROM "+table_name)
        rows = self.cursor.fetchall()
        for row in rows:
            Log().i(row)


# %%

# metadata = Metadata()
# metadata.print_and_validate_data('goes_metadata')


# %%
