# encoding = utf-8
import pyodbc
from decouple import config

conn = pyodbc.connect(config('MSSQL_CONNECT'))
"""
Questa era la vecchia stringa di connessione che adesso gestisco con Python Decouple
    r'DRIVER={SQL Native Client};'
    r'SERVER=HP-PRO3520\SQLEXPRESS_2012;'
    r'DATABASE=Assocam;'
    r'UID=Assocam;'
    r'PWD=Assocam'

"""


def sqlserverinterface(query):
    cursor = conn.cursor()
    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    result = []
    for row in cursor.fetchall():
        result.append(dict(zip(columns, row)))
    return result



""""
    # cursor.execute("select * from [Assocam].[dbo].[g_Users]")
    cursor.execute("select [Anno Formativo] AS anno from [Assocam].[dbo].[Tabella Anni Formativi] "
                   "ORDER BY [Default] DESC, [Anno Formativo] DESC")
    # for row in cursor.fetchall():
    #    print(row)

QUESTA è molto interessante per convertire l'output di pyodbc in un dizionario Django style !
>>> cursor = connection.cursor().execute(sql)
>>> columns = [column[0] for column in cursor.description]
>>> print columns
['name', 'create_date']
>>> results = []
>>> for row in cursor.fetchall():
...     results.append(dict(zip(columns, row)))
...
>>> print results

[{'create_date': datetime.datetime(2003, 4, 8, 9, 13, 36, 390000), 'name': u'master'},
 {'create_date': datetime.datetime(2013, 1, 30, 12, 31, 40, 340000), 'name': u'tempdb'},
 {'create_date': datetime.datetime(2003, 4, 8, 9, 13, 36, 390000), 'name': u'model'},
 {'create_date': datetime.datetime(2010, 4, 2, 17, 35, 8, 970000), 'name': u'msdb'}]

    r = [dict((cursor.description[i][0], value) \
              for i, value in enumerate(row)) for row in cursor.fetchall()]
    
    json_output = json.dumps(r)
    print(json_output)
"""