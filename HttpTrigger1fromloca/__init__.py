import logging
from threading import local
import requests
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import json
import pyodbc
import os
import pandas as pd
#import confi
#connection string for connecting to the database  
cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=mysqlserverlearn.database.windows.net;"
            "Database=mydemosqldb;"
            "UID=myadmin;"
            "PWD=Parth@1997;")
# cnxn_str = os.environ['connectionString']


# databasee = os.environ['database']
# usernamee = os.environ['username'] 
# passwordd = os.environ['password']
# # driverr = os.environ['driver']
# server: "mysqlserverlearn.database.windows.net"
# database : "mydemosqldb"
# username : "myadmin" 
# password : "Parth@1997"
# driver : {SQL Server Native Client 11.0}

# cnxn_str = ('DRIVER=' + driver + 
#                       ';SERVER=' + server + 
#                       ';DATABASE=' + database + 
#                       ';UID=' + username + 
#                       ';PWD=' + password)


api_endpoint = os.environ['apiEndPoint']
#server = os.environ['server']
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    print('Funtion triggered again!')
    #print(type(api_endpoint))
    #print(cnxn_str)
    # print(server)
    result = requests.get(url=api_endpoint)    
    json_data=result.json()     
    #print(x)
    
    Body = json.dumps(json_data)
    a=json.loads(Body)#list 
    df= pd.DataFrame(a,columns=['userId','id','title','body'])
    
    conn = pyodbc.connect(cnxn_str)
    
    cursor = conn.cursor()
    
    for index, row in df.iterrows():
        cursor.execute("insert into newtable (userId,id,title,body) values(?,?,?,?)",row.userId,row.id,row.title,row.body)
    cursor.commit()
    cursor.close()
    conn.close()
    




    #for inserting json file into blob

    '''
    blob_service_client  = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=azurefunctionresour813a;AccountKey=3BSk+AwgH0EVT2Z7IIwAiTRG0/XEwnyoaloznVh9UZVX8gPm1tD7i5LaWVZrSnJvhmDaeST0HA3B+AStUAbPKg==;EndpointSuffix=core.windows.net")
    blob_client = blob_service_client.get_blob_client("myblobcontainer",blob="1.json")
    blob_client.upload_blob(Body)

    print("Upload Completed")
    print(Body)

    conn = pyodbc.connect(cnxn_str)
    
    cursor = conn.cursor()
    try:        
        
        cursor.execute(cursor.execute('EXEC prcInsertEmployees2 @json = ?', Body))
        print('inserted data')    

    except pyodbc.Error as err:
        print('Error !!!!! %s' % err)
    except:
        print('!')
    cursor.commit()
    cursor.close()
    conn.close()
    print('closed db connection')   
    '''
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello,. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
