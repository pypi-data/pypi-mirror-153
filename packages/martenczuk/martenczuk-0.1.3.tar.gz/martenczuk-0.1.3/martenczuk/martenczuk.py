# KAMIL MARTENCZUK 13.03.2022
# FULL ACCESS TO DB TABLES VIEWS AND SCALAR FUNCTION
import json
import csv
import time
import pypyodbc
from tqdm import tqdm

class JSONFile:
    def __init__(self, path, name) -> object:
        self.filepath = path
        self.filename = name
        self.data = json.load(open(self.filepath + '/' + self.filename + '.json'))

class CSVFile:
    def __init__(self, path, name, delimiter) -> object:
        self.filepath = path
        self.filename = name
        self.delim = delimiter
        self.data = csv.reader(open(self.filepath + '/' + self.filename + '.csv', mode='r'), delimiter=self.delim)
        self.array = [x for x in self.data]

class SQLConn:
    def __init__(self, configFile: JSONFile) -> object:
        self.drivers = configFile.data['drivers']
        self.server = configFile.data['server']
        self.port = configFile.data['port']
        self.user = configFile.data['user']
        self.password = configFile.data['password']
        self.database = configFile.data['database']
        self.trustmode = configFile.data['Trusted_Connection']
        self.conn = pypyodbc.connect('DRIVER={' + self.drivers + '};SERVER='+ self.server +';UID='+ self.user +';PWD='+ self.password +';DATABASE='+ self.database +';Trusted_Connection='+ self.trustmode +';')

class SQLObject:
    def __int__(self, schemaName, objectName) -> object:
        self.schema = "[" + schemaName + "]"
        self.object = "[" + objectName + "]"
        self.fullname = self.schema + "." + self.object

def VTE(source: SQLObject, destination: SQLObject, SQLConnection: SQLConn):
    print("\n SQL View " + source + " is converting to SQL Table " + destination + " in database " + SQLConnection.database + ". Please Stand By...\n")
    conn0 = SQLConnection.conn
    cursor = conn0.cursor()
    cols = cursor.execute("""Select [name] from sys.columns WHERE object_id = OBJECT_ID('"""+source+"""')""").fetchall()
    cols_string = cols[0][0]
    for i in range (1,len(cols)):
        cols_string += " , [" + cols[i][0] + "]"
    rows = cursor.execute("""Select ["""+cols[0][0]+"""] from """+source+""" ORDER BY date""").fetchall()
    for i in tqdm(range(len(rows))):
        row = cursor.execute("""Select * from """+source+""" WHERE """+cols[0][0]+"""='"""+rows[i][0]+"""'""").fetchall()
        values_string = "'" + row[0][0] + "'"
        for j in range (1,len(row[0])): values_string += ",'" + str(row[0][j])+"'"
        try:
            cursor.execute(""" Insert into """ + destination + """ (""" + cols_string + """) VALUES (""" + values_string + """)""")
        except:
            pass
        cursor.commit()
        time.sleep(1)
    conn0.close()
    return 0