import unittest
import pandas as pd
import re
import streamlit as st
import sqlite3 as sql
from utils.logger import Log
### Importing MAPS DATA:
def load_data(nrows):
    data = pd.read_fwf('https://www.ncei.noaa.gov/access/homr/file/nexrad-stations.txt', nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data = data.drop(index = 0,axis = 0)
    # data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
# data = pd.read_csv(nexrad-stations.txt)
data = load_data(100000)

df = pd.DataFrame()
df['name']=data['name']
df['county']=data['county']
df['lat'] = data['lat']
df['lon'] = data['lon']
df['elev'] = data['elev']

def map_data_tbl():
    Log().i('Creating database if not exists')
    table_name = 'Mapdata'
    conn = sql.connect('data/GOESmetadata.db')
    cursor = conn.cursor()
    query = f'Create table if not Exists {table_name} (Name,County,Lat,Lon,Elev)'
    cursor.execute(query)
    df.to_sql(table_name,conn,if_exists='replace',index=False)
    return conn,cursor



