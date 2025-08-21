import clickhouse_connect
import datetime
import json
import logging
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

client = clickhouse_connect.get_client(
    host=os.getenv("CLICKHOUSE_HOST", "localhost"),
    username=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", "default"),
    port=os.getenv("CLICKHOUSE_HTTP_PORT", "8123")
)

# Init schema
def init():
    with open("init.sql",'r') as r:
        client.query(r.read())
    
# Insert data
def insert_data(table, data, key):
    try:
        check_dup = client.query(f"""
            SELECT count(*) from {table} where {key} = '{data[key]}'
        """)
        if check_dup.result_rows[0][0] >= 1:
            logging.warning(f"Skip, duplicated hash {data[key]}")
        else:
            column_names = list(data.keys())
            insertedData = [list(data.values())]
            client.insert(table=table, data=insertedData, column_names=column_names)
            logging.info(f"Successfully insert {data[key]}")
    except Exception as e:
        raise Exception(e)
        logging.error(e)

def retrieve_data(column,table):
    try:
        retrieve = client.query(f"SELECT {column} from {table}")
        if len(retrieve.result_rows) > 0:
            return retrieve.result_rows
        else:
            raise Exception("No data found")
    except Exception as e:
        logging.error(e)