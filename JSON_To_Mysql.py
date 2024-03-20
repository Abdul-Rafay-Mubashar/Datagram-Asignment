import pandas as pd
from sqlalchemy import create_engine
import pymysql


df = pd.read_json('Output.json')
database_name = 'mydb'
host = 'localhost'  
# Enter Your Port Number
port = 3306         
user = 'root'
# Enter Your Password
password = '*********'


try:
    connection = pymysql.connect(host=host, port=port, user=user, password=password)
    print("Connection successful!")
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}')
    df.to_sql('db_table', engine, if_exists='replace')
    connection.close()
except Exception as e:
    print(f"Error: {e}")