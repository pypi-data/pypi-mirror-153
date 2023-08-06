# Generic functions which can be reused in every project. 
# .env file needed! ----- Not up to now
from web3 import Web3
from eth_abi import encode_single, encode_abi
from eth_account import Account
from ..utils import helper
import secrets
import requests
import json
import math

headers = {
    'User-Agent': 'NMask User Agent 1.0',
    'From': 'nmask@nmask.com'  # This is another valid field
} 
def create_address():
    '''
    web3_generic method: create public key and private key for ETH and BNB.
    
    Returns
    --------
    list
        first element ist private key, second element ist public key
    '''
    private_key_raw = secrets.token_hex(32)
    private_key = "0x" + private_key_raw
    public_key = Account.from_key(private_key).address
    return [private_key,public_key]

def create_address_from_private_key(private_key:str):
    '''
    web3_generic method: creates public key from private key.

    Parameters
    --------
    private_key : str
        string of private key. No need of leading "0x"

    Returns:
    --------
    list
        first element ist private key, second element ist public key
    '''
    if private_key == None or len(private_key) == 0:
        return [None,None]
    else:
        if private_key[:2] != '0x':
            private_key = "0x" + private_key
        try:
            public_key = Account.from_key(private_key).address
            return [private_key,public_key]
        except Exception as e: 
            print('Private Key Corrupt: Cannot create public key')
            print(e)
            return [None,None]

def get_eth_or_bsc_scan_api_url(chain_id:int):
    '''
    web3_generic method: get the API enpoint URLs for Rinkeby, Etherem Mainnet, BSC Testnet and BSC Testnet

    Parameters
    --------
    chain_id : int
        official chain id (e.g. 1 for Ethereum, 56 for Binance)

    Returns:
    --------
    str
        begin of the Etherscan or Bscscan API endpoint
    '''
    if chain_id == 1:
        url = 'https://api.etherscan.io/api'
    elif chain_id == 3:
        url = 'https://api-ropsten.etherscan.io/api'
    elif chain_id == 4:
        url = 'https://api-rinkeby.etherscan.io/api'
    elif chain_id == 56:
        url = 'https://api.bscscan.com/api'
    elif chain_id == 97:
        url = 'https://api-testnet.bscscan.com/api'
    else:
        return None
    return url

def get_contract_abi_by_eth_or_bsc_scan(contract:str,chain_id:int,api_key:str):
    '''
    web3_generic method: get contract abi

    Parameters
    --------
    contract : str
        contract address
    chain_id : int
        official chain id (e.g. 1 for Ethereum, 56 for Binance)
    api_key : str
        API Key of the Etherscan or Bscscan API endpoint

    Returns:
    --------
    str
        (Default: None) string of contract ABI
    '''
    url = get_eth_or_bsc_scan_api_url(chain_id)
    
    if url != None and len(api_key) != 0 and Web3.isAddress(contract):
        api_url = ''.join([url,'?module=contract&action=getabi&address={0}&tag=latest&apikey={1}'.format(contract,api_key)]) 
        response = requests.get(api_url,headers=headers)
        parsed = json.loads(response.text)
        if parsed['message'] == 'NOTOK':
            print('{0}: {1}'.format(contract,parsed['result']))
            return None
        abi = parsed['result']
        return abi
    return None

def call_contract_function(web3_instance:Web3,contract_address:str,abi:str,contract_function:str,args:list=None):
    '''
    web3_generic method: call a contract function and get return

    Parameters
    --------
    web3_instance : Web3
        initialised Web3 Instance, e.g. with HTTPProvider
    contract_address : str
        contract address
    abi : str
        contract ABI
    contract_function : str
        function name

    Returns:
    --------
    any
        (Default: None) function return
    '''
    if Web3.isAddress(contract_address):
        my_contract = web3_instance.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)
        contract_function = my_contract.functions[contract_function]
        if args == None:
            result = contract_function().call()  
        else:
            result = contract_function(*args).call()  
        return result
    return None

def get_address_balance_by_eth_or_bsc_scan(address:str,chain_id:int,api_key:str,contract_address:str=None):
    '''
    web3_generic method: get ETH/BNB or token balance for address

    Parameters
    --------
    address : str
        address
    chain_id : int
        official chain id (e.g. 1 for Ethereum, 56 for Binance)
    api_key : str
        API Key of the Etherscan or Bscscan API endpoint
    contract_address : str
        (Default: None) contract address of a token

    Returns:
    --------
    int
        (Default: None) ETH/BNB (contract_address=None) or Token (contract_address has value) balance for address. 
    '''
    url = get_eth_or_bsc_scan_api_url(chain_id)
    
    if url != None and len(api_key) != 0 and Web3.isAddress(address):
        if contract_address == None:
            api_url = ''.join([url,'?module=account&action=balance&address={0}&tag=latest&apikey={1}'.format(address,api_key)])
        elif Web3.isAddress(contract_address):
            api_url =''.join([url,'?module=account&action=tokenbalance&address={0}&contractaddress={1}&tag=latest&apikey={2}'.format(address,contract_address,api_key)])
        else:
            return None    

        try:
            response = requests.get(api_url,headers=headers)   
            if response.text == 'The service is unavailable.':
                return None
            return int(json.loads(response.text)['result'])
        except Exception as e:
            print(e)
            return None
    else:
        return None

def get_addresses_balance_by_eth_or_bsc_scan(addresses:list,chain_id:int,api_key:str,token_address:str=None):
    '''
    web3_generic method: get ETH/BNB or token balance for addresslist.

    Parameters
    --------
    address : list
        list of addresses
    chain_id : int
        official chain id (e.g. 1 for Ethereum, 56 for Binance)
    api_key : str
        API Key of the Etherscan or Bscscan API endpoint
    contract_address : str
        (Default: None) contract address of a token

    Returns:
    --------
    dict
        (Default: None) ETH/BNB (contract_address=None) or Token (contract_address has value) balance for addresslist. 
    '''
    url = get_eth_or_bsc_scan_api_url(chain_id)
    
    if url != None and len(api_key) != 0 and len(addresses) != 0:
        for address in addresses:
            if not Web3.isAddress(address):
                return None        
        
        address_with_balance = {}
        # API allows max if 20 Addresses equally:
        for i in range(0,math.ceil(len(addresses)/20)):
            addresses_slice = addresses[int(i*20):int((i+1)*20)]
            if token_address == None:  
                api_url = ''.join([url,'?module=account&action=balancemulti&address={0}&tag=latest&apikey={1}'.format(','.join(addresses_slice),api_key)])    
            try:
                if token_address == None:
                    response = requests.get(api_url,headers=headers)  
                    if response.text == 'The service is unavailable.':
                        return None 
                    for r in json.loads(response.text)['result']:
                        address_with_balance.update({r['account']: int(r['balance'])})
                else:
                    for address in addresses_slice:
                        address_with_balance.update({address: get_address_balance_by_eth_or_bsc_scan(address,
                                chain_id,
                                api_key,
                                token_address
                            )})
                return address_with_balance
            except:
                return None

def get_usd_price_by_eth_or_bsc_scan(chain_id:int,api_key:str):
    '''
    web3_generic method: get ETH/BNB USD Price for timestamp

    Parameters
    --------
    chain_id : int
        official chain id (e.g. 1 for Ethereum, 56 for Binance)
    api_key : str
        API Key of the Etherscan or Bscscan API endpoint

    Returns:
    --------
    dict
        (Default: None) ETH/BNB (contract_address=None) or Token (contract_address has value) balance for addresslist. 
    '''

    url = get_eth_or_bsc_scan_api_url(chain_id)
    if chain_id in [56,97]:
        api_url = ''.join([url,'?module=stats&action=bnbprice&apikey={0}'.format(api_key)])  
    else:
        api_url = ''.join([url,'?module=stats&action=ethprice&apikey={0}'.format(api_key)])     
    
    try:
        response = requests.get(api_url,headers=headers)  
        if response.text == 'The service is unavailable.':
            return None 
        return json.loads(response.text)['result']
    except Exception as e:
        print(e)
        return None


def build_contract_transaction(web3_instance:Web3,contract_address:str,abi:str,tx:dict,function:str,function_args:list): 
    if Web3.isAddress(contract_address):
        my_contract = web3_instance.eth.contract(address=contract_address, abi=abi)
        contract_function = my_contract.functions[function]
        return contract_function(*function_args).buildTransaction(tx)
    return None

def send_transaction(web3_instance:Web3,chain_id:int,tx:dict,private_key:str,nonce_with_offset:int=None):
    '''
    web3_generic method: send simple transaction 

    Parameters
    --------
    web3_instance : Web3
        initialised Web3 Instance, e.g. with HTTPProvider
    chain_id : int
        official chain id (e.g. 1 for Ethereum, 56 for Binance)
    tx : dict
        dictionary with transaction keys (e.g. value,from,to,etc.) and respective values.
    private_key : str
        private key of send address, to sign transaction
    nonce_offset : int
        (Default: 0) For multiple transactions, Nonce has to to be calculated with fixed nonce parameter and offset

    Returns:
    --------
    str
        (Default: None) transaction hash when successful
    '''
    if nonce_with_offset != None:
        tx['nonce'] = int(nonce_with_offset)
    else:
        tx['nonce'] = int(web3_instance.eth.getTransactionCount(create_address_from_private_key(private_key)[1]))
    # maybe deprecated
    tx['chainId'] = chain_id
    #sign the transaction
    print(tx)
    signed_tx = web3_instance.eth.account.sign_transaction(tx, private_key)
    #send transaction
    try:
        tx_hash = web3_instance.eth.sendRawTransaction(signed_tx.rawTransaction)
        #get transaction hash
        return web3_instance.toHex(tx_hash)
    except Exception as e: 
        print(e)
        return None

def get_base_fee(web3_instance:Web3,chain_id:int):
    if chain_id == 56 or chain_id == 97:
        return None
    try:
        block = web3_instance.eth.get_block('latest')
        return {
            'timestamp': block['timestamp'],
            'number': block['number'],
            'baseFeePerGas': block['baseFeePerGas']
        }
    except Exception as e:
        print(e)
        return None

def get_liquidity_pool_address(w3:Web3,swap_contract_address:str,swap_contract_abi:str,chain_id:int,token0_address:str,token1_address:str,prodEnv:bool=True):
    swap_contract = w3.eth.contract(address=swap_contract_address, abi=swap_contract_abi)
    swap_contract_factory_address = swap_contract.functions.factory().call()
    swap_contract_factory_abi = helper.getABI(swap_contract_factory_address,chain_id,prodEnv)
    swap_contract_factory = w3.eth.contract(address=swap_contract_factory_address, abi=swap_contract_factory_abi)
    try:
        return swap_contract_factory.functions.getPair(token0_address,token1_address).call()
    except Exception as e:
        return None

        