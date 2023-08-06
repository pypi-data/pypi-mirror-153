import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json
from RupineWeb3Utils.utils import payloadBuilder

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

def post(url, apiKey:str,credentials_name:str,credentials_type:str,credentials_value:str,chain_id:int,env_url_arg:str=''):
    local_url = url.format(apiKey,env_url_arg)
    payload = {  
        "credentials_name":credentials_name,
        "credentials_type":credentials_type,
        "credentials_value":credentials_value,
        "chain_id": chain_id
    }

    #return requests.request("POST", local_url, headers=headers, data=json.dumps(payload))
    return session.post(local_url, headers=headers, data=json.dumps(payload))

def put(url, apiKey:str,env_url_arg:str='',payload:dict={}):
    local_url = url.format(apiKey,env_url_arg)
    if payload == {}:
        #return requests.request("PUT", local_url, headers=headers)
        return session.put(local_url, headers=headers)
    else:
        #return requests.request("PUT", local_url, headers=headers, data=json.dumps(payload))
        return session.put(local_url, headers=headers, data=json.dumps(payload))

def get_credential(url, api_key, credential_name:str,credential_type:str,chain_id:int,prodEnv:bool=True):
    return "abc:def"
    