from itertools import count
import sys
import psycopg2
import json
import random
import calendar
import time
import pandas as pd
import json
from datetime import datetime
from psycopg2.extras import LogicalReplicationConnection


try:
    my_connection  = psycopg2.connect(
                      "dbname='ADTTest' host='localhost' user='ashmijoseph' password='password'" ,
                      connection_factory = LogicalReplicationConnection)
    print(my_connection)
    
except Exception as e:
    print(str(e))
    print("ERROR: Unexpected error: Could not connect to PostgreSQL instance.")
    sys.exit()



def handler():
    cur = my_connection.cursor()
    try:
        cur.create_replication_slot('wal2json_test_slot', output_plugin = 'wal2json')
    except:
        pass
    cur.start_replication(slot_name = 'wal2json_test_slot', options = {'pretty-print' : 1}, decode= True)
    
    cur.consume_stream(consume)

overall_rows = []
columns_names = None

def consume(msg):
    FILE_LOCATION = '/Users/ashmijoseph/Desktop/ASHMI_DOCS/MAC/Winter-2022/ADT/Project/'

    print (msg.payload)
    data_incoming = msg.payload
    data_incoming = json.loads(data_incoming)
    print(data_incoming)
    print('----------------------------')
    if len(data_incoming.get('change'))> 0:
        columns_names = data_incoming.get('change')[0].get('columnnames')
        columns_values = data_incoming.get('change')[0].get('columnvalues')
        table_name = data_incoming.get('change')[0].get('table')
        kind = data_incoming.get('change')[0].get('kind')
        columns_names.append('kind')
        columns_values.append(kind)
        print(columns_names)
        print(columns_values)
        FILE_LOCATION = FILE_LOCATION + table_name + '.csv'
        try :
            df = pd.read_csv(FILE_LOCATION, index_col = False)
            df_delta = pd.DataFrame([columns_values], columns= columns_names)
            df = df.append(df_delta,ignore_index = True)
            df.to_csv(FILE_LOCATION, index=False)
            #user_input = input("DO you wish to continue")
        except Exception as e: 
            print(str(e))
            print('EXCEPTION')
            df = pd.DataFrame([columns_values], columns= columns_names)
            df.to_csv(FILE_LOCATION,index = False)




    

    #df = pd.CreateDataFrame()

handler()
# df = pd.DataFrame(overall_rows, columns= columns_names)
# df.to_csv('/Users/ashmijoseph/Desktop/ASHMI_DOCS/MAC/Winter-2022/ADT/Project/test.csv')