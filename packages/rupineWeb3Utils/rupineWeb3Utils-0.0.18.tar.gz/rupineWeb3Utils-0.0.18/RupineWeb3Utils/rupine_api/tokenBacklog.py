import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json
from web3 import Web3
from cfc_package.neblmask_api import tokenObjects,payloadBuilder

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

# def post(apiKey:str,token_address:str,liquidity_pool_address:str,buyAmount:int,is_active:str,
#     is_completed:str,chain_id:int,env_url_arg:str=''):
#     local_url = url.format(apiKey,env_url_arg)
#     payload = {  
#         "token_address": token_address,
#         "liquidity_pool_address":liquidity_pool_address,
#         "buy_amount":buyAmount,
#         "is_active":is_active,
#         "is_completed":is_completed,
#         "chain_id":chain_id,
#     }
#     return requests.request("POST", local_url, headers=headers, data=json.dumps(payload))

def put(url:str, apiKey:str,env_url_arg:str='',payload:dict={}):
    local_url = url.format(apiKey,env_url_arg)
    if payload == {}:
        return session.put(local_url, headers=headers)
    else:
        return session.put(local_url, headers=headers, data=json.dumps(payload))
  

def updateCodeCheck(tokenAddress:str,neblMaskApiKey:str,env_url_arg:str):
    response = tokenObjects.get_codecheck(apiKey=neblMaskApiKey,
    token_address=Web3.toChecksumAddress(tokenAddress),
    env_url_arg=env_url_arg)
        
    result = json.loads(response.text)
    if len(result) != 0:
        check_result = 2
        if int(result[0]['is_edited_y']) == int(result[0]['is_malicious_n']) and int(result[0]['is_edited_n']) == 0:
            check_result = 1
        if int(result[0]['is_malicious_y']) > 0:
            check_result = 3
        payload = payloadBuilder.put([['contract_address',Web3.toChecksumAddress(tokenAddress),'eq']],[['code_check_result',str(check_result)]])
        put(apiKey=neblMaskApiKey,env_url_arg=env_url_arg,payload=payload)