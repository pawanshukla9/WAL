from itertools import count
import sys
import psycopg2
import json
import pandas as pd
from psycopg2.extras import LogicalReplicationConnection


try:
    #Create a new database session and return a new connection object
    my_connection  = psycopg2.connect(
                      "dbname='ADTTest' host='localhost' user='ashmijoseph' password='password'" ,
                      connection_factory = LogicalReplicationConnection)
    print(my_connection)
    
except Exception as e:
    print(str(e))
    print("ERROR: Unexpected error: Could not connect to PostgreSQL instance.")
    sys.exit()



def handler():
    #Cursors allow to execute PostgreSQL command in a database session
    cur = my_connection.cursor()
    try:
        cur.create_replication_slot('wal2json_test_slot', output_plugin = 'wal2json') #Create a logical replication slot
    except:
        pass
    cur.start_replication(slot_name = 'wal2json_test_slot', options = {'pretty-print' : 1}, decode= True) #Instructs server to start streaming WAL
    
    cur.consume_stream(consume)
    # ^^^ endless loop or stream: stop with Control-C

overall_rows = []
columns_names = None

def consume(msg):
    FILE_LOCATION = '/Users/ashmijoseph/Desktop/ASHMI_DOCS/MAC/Winter-2022/ADT/Project/WAL/'
    print (msg.payload)
    print('----------------------------')
    data_incoming = msg.payload
    #parse the JSON string and convert it into a Dictionary.
    data_incoming = json.loads(data_incoming)
    print(data_incoming)
    print('----------------------------')
    if len(data_incoming.get('change'))> 0:
        columns_names = data_incoming.get('change')[0].get('columnnames') #get columnNames
        columns_values = data_incoming.get('change')[0].get('columnvalues') #get columnValues
        table_name = data_incoming.get('change')[0].get('table') #get DB tableName
        kind = data_incoming.get('change')[0].get('kind') #get DB operation performed
        columns_names.append('kind')
        columns_values.append(kind)
        FILE_LOCATION = FILE_LOCATION + table_name + '.csv' #create a separate csv file for each table
        try :
            df = pd.read_csv(FILE_LOCATION, index_col = False) #Read a csv file into DataFrame
            df_delta = pd.DataFrame([columns_values], columns= columns_names)
            df = df.append(df_delta,ignore_index = True)
            df.to_csv(FILE_LOCATION, index=False) #Write object to a csv file
        except Exception as e: 
            print(str(e))
            print('EXCEPTION')
            df = pd.DataFrame([columns_values], columns= columns_names)
            df.to_csv(FILE_LOCATION,index = False)

handler()