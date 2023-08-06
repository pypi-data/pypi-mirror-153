import json
from web3 import Web3
from web3.contract import Contract

def get_contract_event_in_transaction(contract:Contract, txHash:str,eventName:str):

    # Web3.py scheint es nicht zu können events string basiert abzurufen.
    # e.g. contract.events['Transfer']
    # Es ist notwendig immer einer Funktionsaufruf abzusetzen
    # e.g. contract.events.Transfer()
    # Um dies zu umschiffen wird hier dynamisch Code erzeugt und ausgeführt

    code = '''def getEvent():
    try:
        c = contract.events.{0}()
        return c
    except:
        return None
c = getEvent()
        '''.format(eventName)

    d = {}
    exec(code, {'contract': contract}, d)
    contractEvent = d['c']
    return contractEvent

# returns <tokenClass>,<verified>
def check_contract_standard(contract:Contract):
    if not contract:
        return ['n/a', 'N']
    if not contract.abi:
        return ['n/a', 'N']

    # Check ABI if ERC20 or ERC721 interface  functions are implemented with correct name, input and output parameter
    # ERC20 check according to: https://eips.ethereum.org/EIPS/eip-20
    abi = contract.abi

    #print(abi)

    ERC20Checklist = []
    # Mandafory: Function totalSupply
    ERC20Checklist.append({ "Check": False, "type": "'type': 'function'", "name": "'name': 'totalSupply'"})
    # Mandafory: Function BalanceOf
    ERC20Checklist.append({ "Check": False, "type": "'type': 'function'", "name": "'name': 'balanceOf'"})
    # Mandafory: Function transfer
    ERC20Checklist.append({ "Check": False, "type": "'type': 'function'", "name": "'name': 'transfer'"})
    # Mandafory: Function allowance
    ERC20Checklist.append({ "Check": False, "type": "'type': 'function'", "name": "'name': 'allowance'"})
    # Mandafory: Function approve
    ERC20Checklist.append({ "Check": False, "type": "'type': 'function'", "name": "'name': 'approve'"})
    # Mandafory: Function transferFrom
    ERC20Checklist.append({ "Check": False, "type": "'type': 'function'", "name": "'name': 'transferFrom'"})
    # Mandafory: Event Transfer
    ERC20Checklist.append({ "Check": False, "type": "'type': 'event'", "name": "{'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'from', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'to', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'Transfer', 'type': 'event'}"})
    # Mandafory: Event Approval
    ERC20Checklist.append({ "Check": False, "type": "'type': 'event'", "name": "{'anonymous': False, 'inputs': [{'indexed': True, 'internalType': 'address', 'name': 'owner', 'type': 'address'}, {'indexed': True, 'internalType': 'address', 'name': 'spender', 'type': 'address'}, {'indexed': False, 'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}], 'name': 'Approval', 'type': 'event'}"})

    ERC721Checklist = []
    ERC721Checklist.append({ "Check": False, "name": "some placeholder here"})

    for line in abi:
        for item in ERC20Checklist:
            if  str(item['name']) in str(line) and str(item['type']) in str(line):
                item['Check'] = True
        for item in ERC721Checklist:
            #print(line)
            #print("..................")
            #print(item['ABILine'])
            #print("-----------------------------")
            #print("NEXT LINE")
            #print("-----------------------------")
            if  str(item['name']) in str(line) and str(item['type']) in str(line):
                item['Check'] = True
            
    isERC20 = True
    for item in ERC20Checklist:
        isERC20 = isERC20 and item['Check']
    if isERC20:
        return ['ERC20','Y']

    isERC721 = True
    for item in ERC20Checklist:
        isERC721 = isERC721 and item['Check']
        #if item['Check']:
        #    print('Check')
        #else:
        #    print(item['ABILine'])
    if isERC721:
        return ['ERC20','Y']

    return ['n/a','Y']
