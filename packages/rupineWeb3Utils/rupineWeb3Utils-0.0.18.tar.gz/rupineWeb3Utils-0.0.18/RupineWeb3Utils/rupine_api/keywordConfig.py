import requests
from flask.wrappers import Response
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json

headers = {
    'Content-Type': 'application/json'
    }
session = requests.Session()
retry = Retry(connect=5,backoff_factor=0.2)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def get(url:str, apiKey:str,env_url_arg:str='',payload:dict={}):
    local_url = url.format(apiKey,env_url_arg)
    if payload == {}:
        return session.get(local_url, headers=headers)
        #return requests.request("GET", )
    else:
        return session.get(local_url, headers=headers, data=json.dumps(payload))
        #return requests.request("GET", local_url, headers=headers, data=json.dumps(payload))

def post(url:str, apiKey:str,keyword:str,keyword_detail:str,reference:str,method:str,value:str,message:str,env_url_arg:str=''):
    local_url = url.format(apiKey,env_url_arg)
    payload = {  
        "keyword": keyword,
        "keyword_detail": keyword_detail,
        "reference": reference,
        "method":method,
        "message": message,
        "value":value
    }

    #return requests.request("POST", local_url, headers=headers, data=json.dumps(payload))
    return session.post(local_url, headers=headers, data=json.dumps(payload))

def put(url:str, apiKey:str,env_url_arg:str='',payload:dict={}):
    local_url = url.format(apiKey,env_url_arg)
    if payload == {}:
        #return requests.request("PUT", local_url, headers=headers)
        return session.put(local_url, headers=headers)
    else:
        #return requests.request("PUT", local_url, headers=headers, data=json.dumps(payload))
        return session.put(local_url, headers=headers, data=json.dumps(payload))

def delete(url:str, apiKey:str,payload:dict,env_url_arg:str=''):
    local_url = url.format(apiKey,env_url_arg)
    if payload != {}:
        return session.delete(local_url, headers=headers, data=json.dumps(payload))
    return Response(status=400)
