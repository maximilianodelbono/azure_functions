import logging
import azure.functions as func
import os
from dotenv import load_dotenv
import json

import sys
sys.path.insert(1, '/')
from dbpostgres import get_clients,addTest,includeAlert


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        load_dotenv(".\.env")
    except:
        pass
   
    #convert the request to somehting that we can read.
    request=req.get_json()

    #are they attaching a token?
    token = request['token']

    #Unauthorized API call
    if 'token' not in request.keys():
        response={'Status':'401','Message':'Unauthorized API call.'}
        return func.HttpResponse(json.dumps(response))
    elif token != os.environ['TOKEN']:
        response={'Status':'403','Message':'You shall not pass.'}
        return func.HttpResponse(json.dumps(response))
    elif token == os.environ['TOKEN']:
        #authorized call.
        
        #check what has been sent to the function
        ccn=request['ccn']
        over=request['overdraft']
        stolen=request['stolen']
        try: 
            event=request['event']
        except:
            event='testing-default'
        
        #getallclients
        #print(get_clients())

        if stolen==True:
            print(includeAlert(stolen=stolen))
        elif over==True:
            (includeAlert(overdraft=over))
        
        #add the event and return to the test
        print(addTest(event))
        json_obj=f"You tested with credit card #: {ccn}, overdraft: {over}, stolen: {stolen}. Event: {event}"
        return func.HttpResponse(json_obj, status_code=200, mimetype="application/json")