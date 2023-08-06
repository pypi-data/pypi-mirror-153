import requests
from web3 import Web3
import json
import numpy as np
import urllib.parse as urlparse
import time

from ..utils import helper
from ..web3_utils import web3_globals

def is_list_of_addresses(self,address_list:str):    
    '''
    web3_generic method: send simple transaction 

    Parameters
    --------
    address_list : str
        comma separated list of addresses
    
    Returns:
    --------
    bool
        False if at least one address in address list is not a valid Web3 Address
    '''
    list = address_list.split(',')
    for item in list:
        if not Web3.isAddress(item):
            return False
    return True

def get_lp_pool_of_contract(w3:Web3,chain_id:int,contract_address:str):
    swap_contract_factory_abi = helper.get_abi(w3.toChecksumAddress(web3_globals.AddrUniSwapV2FactoryAdress),chain_id)
    swap_contract_factory_instance = w3.eth.contract(address=w3.toChecksumAddress(web3_globals.AddrUniSwapV2FactoryAdress), abi=swap_contract_factory_abi)
    WETH_contract_address = w3.toChecksumAddress(web3_globals.get_address_weth_or_wbnb(chain_id,w3))
    
    lp_contract_address = swap_contract_factory_instance.functions.getPair(WETH_contract_address,w3.toChecksumAddress(contract_address)).call()
    return lp_contract_address

def get_lp_pool_reserves(w3:Web3,chain_id:int,lp_contract_address:str, prodEnv:bool=True, blocknumber='latest'):
    lp_contract_abi = helper.getABI(w3.toChecksumAddress(lp_contract_address),chain_id,prodEnv)
    lp_contract_instance = w3.eth.contract(address=w3.toChecksumAddress(lp_contract_address), abi=lp_contract_abi)
    reserves = lp_contract_instance.functions.getReserves().call(None, blocknumber)
    result = {
        'blockTimestamp': reserves[2]
    }
    token0_address = lp_contract_instance.functions.token0().call()
    if token0_address == web3_globals.get_address_weth_or_wbnb(chain_id,w3):
        result.update({
            'WETH': reserves[0],
            'Token': reserves[1]
        })
    else:
        result.update({
            'WETH': reserves[1],
            'Token': reserves[0]
        })

    return result

def get_contract_info(w3:Web3,chain_id:int,contract_address:str,function_name:str,abi:str=None,args:list=[],blockNumber=None):
    if abi == None:
        contract_abi = helper.get_abi(w3.toChecksumAddress(contract_address),chain_id)
    else:
        contract_abi = abi
    contract_instance = w3.eth.contract(address=w3.toChecksumAddress(contract_address), abi=contract_abi)
    function_instance = contract_instance.functions[function_name]
    if args == []:
        return function_instance().call()
    else:
        if blockNumber != None:
            return function_instance(*args).call(block_identifier=blockNumber)
        else:
            return function_instance(*args).call()

def gini(array):
    """Calculate the Gini coefficient of a numpy array."""
    # based on bottom eq: http://www.statsdirect.com/help/content/image/stat0206_wmf.gif
    # from: http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    array = array.flatten() #all values are treated equally, arrays must be 1d
    if np.amin(array) < 0:
        array -= np.amin(array) #values cannot be negative
    array += 0.0000001 #values cannot be 0
    array = np.sort(array) #values must be sorted
    index = np.arange(1,array.shape[0]+1) #index per array element
    n = array.shape[0]#number of array elements
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array))) #Gini coefficient


def get_token_holder(contract_address:str,covalent_api_key:str,max_working_time_sec:int):
    headers = {
    'Content-Type': 'application/json'
    }

    covalent_api_key = 'ckey_5625cf364c744bcb8116949ce76'
    
    #https://api.covalenthq.com/v1/1/tokens/
    #0x8b3192f5eebd8579568a2ed41e6feb402f93f73f/
    #match=%7B%22balance%22%3A%7B%22%24gt%22%3A0%7D%7D&sort=%7B%22balance%22%3A+-1%7D&key=ckey_5625cf364c744bcb8116949ce76" \
    match = {"balance":{"$gt":0}}
    sort = {"balance": -1}

    total_supply = 0
    total_supply_minus_burn = 0
    total_supply_api = 0
    token_holder = 0
    token_holder_api = 0
    holdings = []
    page = 0
    begin = time.time()
    while True:

        url = 'https://api.covalenthq.com/v1/1/tokens/{0}/token_holders/?page-number={1}&page-size=1000&match={2}&sort={3}&key={4}'.format(contract_address,page,urlparse.quote_plus(json.dumps(match)),urlparse.quote_plus(json.dumps(sort)),covalent_api_key)
        begin_loop = time.time()
        response = requests.request('GET',url,headers=headers)
        result = json.loads(response.text)
        total_supply_api = int(result['data']['items'][0]['total_supply'])
        token_holder_api = int(result['data']['pagination']['total_count'])
        if len(result) == 0:
            return []
        
        for item in result['data']['items']:
            if item['address'][0:20] == '0x000000000000000000':
                total_supply+= int(item['balance'])
            else:
                total_supply+= int(item['balance'])
                total_supply_minus_burn+= int(item['balance'])
                token_holder+=1
                holdings.append(float(item['balance']))
        end_loop = time.time()
        if (end_loop - begin_loop) + (end_loop - begin) > max_working_time_sec:
            break 
        elif not result['data']['pagination']['has_more']:
            break
        else:
            page+= 1
    gini_coefficient = gini(np.array(holdings))
    #print('Token Holder (perc loaded): {0}-{1} ({2} perc)'.format(token_holder_api,token_holder,100*token_holder/token_holder_api))
    #print('total supply: {0} {1}'.format(total_supply,total_supply_api))
    #print('total supply minus burn: {0} ({1} perc)'.format(total_supply_minus_burn,100*total_supply_minus_burn/total_supply))
    #print('Gini coefficient: {0}'.format(gini_coefficient))
    return {
        'token_holder_api': token_holder_api,
        'token_holder_count': token_holder,
        'total_supply_api': total_supply_api,
        'total_supply_sum': total_supply,
        'total_supply_sum_minus_burn': total_supply_minus_burn,
        'gini_coefficient': gini_coefficient
    }

#get_token_holder('0x96150e34f8b56b59a53c2caab4510edb3085d070','ckey_5625cf364c744bcb8116949ce76',20)


def get_initial_lp_pool_reserves(w3:Web3,chain_id:int,lp_contract_address:str,starting_block:str,ending_block:str):
    headers = {
    'Content-Type': 'application/json'
    }

    covalent_api_key = 'ckey_5625cf364c744bcb8116949ce76'
    #sort = {"block_height": -1, "log_offset": -1}
    topic = '0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1'
    #url = "https://api.covalenthq.com/v1/1/events/topics/{0}/?starting-block={1}&ending-block=13487690&sender-address={2}&page-size=5&sort={3}&key={4}".format(topic,starting_block,lp_contract_address,urlparse.quote_plus(json.dumps(sort)),covalent_api_key)
    url = "https://api.covalenthq.com/v1/1/events/topics/{0}/?starting-block={1}&ending-block={2}&sender-address={3}&page-size=5&key={4}".format(topic,starting_block,ending_block,lp_contract_address,covalent_api_key)
    response = requests.request('GET',url,headers=headers)
    result = json.loads(response.text)
    
    reserves = [0,0]
    reserves_raw = result['data']['items'][0]['decoded']['params']
    for r in reserves_raw:
        if r['name'] == "reserve0":
            reserves[0] = int(r['value'])
        else:
            reserves[1] = int(r['value'])
    
    result = {}
    lp_contract_abi = helper.get_abi(w3.toChecksumAddress(lp_contract_address),chain_id)
    lp_contract_instance = w3.eth.contract(address=w3.toChecksumAddress(lp_contract_address), abi=lp_contract_abi)
    token0_address = lp_contract_instance.functions.token0().call()
    
    if token0_address == web3_globals.get_address_weth_or_wbnb(chain_id,w3):
        result.update({
            'WETH': reserves[0],
            'Token': reserves[1]
        })
    else:
        result.update({
            'WETH': reserves[1],
            'Token': reserves[0]
        })

    return result

# w3 =GetProviderAnkr(1)
# begin = time.time()
# lp = get_lp_pool_of_contract(w3,1,'0xB161D34E6E1E46170d156C8D9809EEaD4e8bc4Fd')
# print(get_initial_lp_pool_reserves(w3,1,lp,13405216,13405416))
# end = time.time()
# print(end-begin)