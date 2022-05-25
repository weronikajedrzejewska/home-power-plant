import datetime
import pandas as pd
from sma_sunnyboy import *
from credentials.config import SMA_PASSWORD, INVERTER_CONNECTION_STRING, INVERTER_IP
import psycopg2
from sqlalchemy import create_engine

IP = INVERTER_IP

USE_SSL = True
PORT = 443

Key.productivity_day = {'tag': '6400_00262200'}

client = WebConnect(IP, Right.USER, SMA_PASSWORD, PORT, USE_SSL)

auth = client.auth()

dictionary = {
    "productivity_day": client.get_value(Key.productivity_day),
    "productivity_total": client.get_value(Key.productivity_total),
    "current_power": client.get_value(Key.power_current),
}
rows = [[datetime.date.today(), client.get_value(Key.productivity_day), client.get_value(Key.productivity_total)]]

columns = ['Date', 'Productivity day', 'Productivity total']
inverter = pd.DataFrame(rows, columns=columns)
inverter.set_index('Date')

conn_string = INVERTER_CONNECTION_STRING

db = create_engine(conn_string)
conn = db.connect()

inverter.to_sql('inverter', con=conn, if_exists='append', index=True, method='multi')

conn = psycopg2.connect(conn_string)
conn.autocommit = True
cursor = conn.cursor()

sql1 = '''select * from inverter;'''
cursor.execute(sql1)

conn.close()

client.logout()
