``` Python

# DECLARATION
import json
import psycopg2
import io
import pandas as pd
import os
os.getcwd()


# READ THE MERGED_GRID CSV FILE IN PANDAS
grid = pd.read_csv("/Users/williamadriel/Desktop/Yara/merged_grid.csv")
grid.head()


# FUNCTION TO BULK LOAD THE DATA IN DATAFRAME TO THE DATABASE
def to_pg(df, conn, cur, table_name):
    """Bulk load data in a dataframe to the connected database.
    Params:
        (pandas dataframe) Dataframe to be loaded into the database
        (connection object) Created from the engine.raw_connection() function
        (cursor object) Created from the conn.cursor() function
        (str) Name of the target table to load the data to
    Returns:
        None
    """
    # generate an in-memory stream for text I/O
    output = io.StringIO()
    # save the dataframe as text buffer in the stream
    df.to_csv(output, sep='\t', header=False, index=False)
    # set the stream position to the start of the stream
    output.seek(0)
    # copy output to the target table in the db (null values become '')
    cur.copy_from(output, table_name, null="")
    # commit to save the changes in the db table
    conn.commit()
    # close stream object and discard the text buffer
    output.close()
    
    
# WRITE THE DATA INTO THE DESIRED TABLE IN THE LOCAL DATABASE (TABLE MUST HAVE SAME VARIABLE AS THE CSV COLUMN)
# Port is extremely important to connect to the database, as well as the dbname, hostname, password and the user.
conn = psycopg2.connect(dbname="postgres", user="postgres", host="localhost",port = 5433, password = '1234')
cur = conn.cursor()
to_pg(grid,conn,cur,'public.grid')



```
