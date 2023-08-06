from web3 import Web3

###################################################################
# Global variables ################################################
###################################################################


# Ankr
url_ankr_eth = 'https://{0}@apis-sj.ankr.com/{1}/eth/fast/main'
url_ankr_bsc = 'https://{0}@apis-sj.ankr.com/{1}/binance/full/main'
url_ankr_ftm = 'https://{0}@apis-sj.ankr.com/{1}/fantom/full/main'
url_ankr_avax = 'https://{0}@apis-sj.ankr.com/{1}/avax/archive/main'
url_ankr_matic = 'https://{0}@apis-sj.ankr.com/{1}/polygon/full/main'

# other provider endpoints
url_infura_rinkeby='https://rinkeby.infura.io/v3/{0}'
url_infura_eth_mainnet='https://mainnet.infura.io/v3/{0}'
url_binance_bsc_testnet='https://data-seed-prebsc-1-s1.binance.org:8545/'
url_binance_bsc_mainnet='https://bsc-dataseed.binance.org/'
url_defibit_bsc_mainnet='https://bsc-dataseed1.defibit.io/'
url_ninicoin_bsc_mainnet='https://bsc-dataseed1.ninicoin.io/'
url_getblock_bsc_mainnet='https://bsc.getblock.io/mainnet/?api_key={0}'
url_getblock_bsc_testnet='https://bsc.getblock.io/testnet/?api_key={0}'
url_getblock_eth_mainnet='https://eth.getblock.io/mainnet/?api_key={0}' 

# Addresses of interest
AddrUniSwapV2FactoryAdress = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
unicryptContractAddr = '0x663A5C229c09b049E36dCc11a9B0d4a8Eb9db214'
AddrLP_uniswapV2 = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
AddrLP_uniswapV3 = '0xe592427a0aece92de3edee1f18e0157c05861564'
AddrLP_sushiSwap = '0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f'
AddrPancakeSwap = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
AddrWETH = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
AddrWBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'

def get_address_weth_or_wbnb(chain_id, w3:Web3):
    if chain_id == 1:
        return w3.toChecksumAddress(AddrWETH)
    elif chain_id == 56:
        return w3.toChecksumAddress(AddrWBNB)
    return None

def get_address_swap_router(chain_id, w3:Web3):
    if chain_id == 1:
        return w3.toChecksumAddress(AddrLP_uniswapV2)
    elif chain_id == 56:
        return w3.toChecksumAddress(AddrPancakeSwap)
    return None

def get_address_uniswapV3_router(chain_id, w3:Web3):
    if chain_id == 1:
        return w3.toChecksumAddress(AddrLP_uniswapV3)
    return None