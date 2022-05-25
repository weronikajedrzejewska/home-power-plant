import datetime
import elicznik
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from credentials.config import USERNAME, TAURON_PASSWORD, METER_ID, CONNECTION_STRING

TODAY = datetime.date.today()
LAST_30_DAYS = datetime.date.today() - datetime.timedelta(days=30)

username = USERNAME
password = TAURON_PASSWORD
meter_id = METER_ID

rows = []

with elicznik.ELicznik(username, password) as licznik:
    readings = licznik.get_readings(LAST_30_DAYS, TODAY)
    for timestamp, consumed, produced in readings:
        rows.append([timestamp, consumed, produced])

columns = ['Date', 'Consumed energy', 'Produced energy']
energy = pd.DataFrame(rows, columns=columns)
energy.set_index('Date', inplace=True)

conn_string = CONNECTION_STRING

db = create_engine(conn_string)
conn = db.connect()

energy.to_sql('data', con=conn, if_exists='replace', index=True, method='multi')

conn = psycopg2.connect(conn_string)
conn.autocommit = True
cursor = conn.cursor()

sql1 = '''select * from data;'''
cursor.execute(sql1)
for i in cursor.fetchall():
        print(i)

conn.close()

