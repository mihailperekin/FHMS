import pandas as pd   #  pip install pandas
import sqlite3

conn = sqlite3.connect('instance\sss.db')
df = pd.read_sql('select * from Users', conn)
df.to_excel('result.xlsx', index=False)