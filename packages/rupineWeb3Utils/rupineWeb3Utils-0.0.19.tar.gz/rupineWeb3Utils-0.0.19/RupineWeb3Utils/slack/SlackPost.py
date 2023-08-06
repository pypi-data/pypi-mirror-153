import json
import sys
import random
import requests
from requests.structures import CaseInsensitiveDict

def SlackPostCreatePair(urlCreatePair, newTokenAddr, hcResult, tokenName, tokenSymbol):

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    msgTokenA = 'New Token: <https://etherscan.io/address/{0}|{1}>'.format(newTokenAddr,newTokenAddr)
    honeypotLink = 'Link <https://honeypot.is/ethereum.html?address={0}|Honeypot.is>'.format(newTokenAddr)
    dexLink = 'Link <https://www.dextools.io/app/ether/pair-explorer/{0}|DexTools.io'.format(newTokenAddr)

    slack_data = {
        "blocks": 
        [
            {"type": "header","text": {"type": "plain_text","text": "New Pair created - {0} ({1})".format(tokenName, tokenSymbol),"emoji": True}},
            {"type": "section","fields": [{"type": "mrkdwn","text": msgTokenA,}]},
            {"type": "section","fields": [{"type": "mrkdwn","text": honeypotLink,}]},
            {"type": "section","fields": [{"type": "mrkdwn","text": dexLink,}]},
            {"type": "section","fields": [{"type": "mrkdwn","text": str(hcResult),}]}
        ]
    }

    data=json.dumps(slack_data)
    resp = requests.post(urlCreatePair, headers=headers, data=data)

def SlackPostNewContract(url, tokenName:str, tokenSymbol:str, address:str, txHash:str, blockNr:str, tokenClass:str, hcResult):

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    #if tokenClass == "ERC20":
    #    resp = requests.post(url, headers=headers, data=data)
    #    print(resp.status_code)

    txHashLink = 'TX Hash: <https://etherscan.io/tx/{0}|{1}>'.format(txHash,txHash)
    addressLink = 'Address: <https://etherscan.io/address/{0}|{1}>'.format(address,address)
    honeypotLink = 'Link <https://honeypot.is/ethereum.html?address={0}|Honeypot.is>'.format(address)
    dexLink = 'Link <https://www.dextools.io/app/ether/pair-explorer/{0}|DexTools.io'.format(address)
    slack_data = {
        #"username": "NotificationBot",
        #"icon_emoji": ":satellite:",
        #"channel" : "#somerandomcahnnel",
        "blocks": [
            {"type": "header","text": {"type": "plain_text","text": "New Contract - {0} ({1})".format(tokenName, tokenSymbol),"emoji": True}},
            {"type": "section","fields": [{"type": "mrkdwn","text": txHashLink,}]},
            {"type": "section","fields": [{"type": "mrkdwn","text": addressLink,}]},
            {"type": "section","fields": [{"type": "plain_text","text": 'Block: {0}'.format(blockNr),}]},
            {"type": "section","fields": [{"type": "plain_text","text": 'Token: {0}'.format(tokenClass),}]},
            {"type": "section","fields": [{"type": "mrkdwn","text": honeypotLink,}]},
            {"type": "section","fields": [{"type": "mrkdwn","text": dexLink,}]},
            {"type": "section","fields": [{"type": "mrkdwn","text": str(hcResult),}]}
        ]
    }

    data=json.dumps(slack_data)

    if tokenClass == "ERC20" or tokenClass == "ERC20 (not verified)":
        resp = requests.post(url, headers=headers, data=data)

def SlackPostLiquidity(url, methodName:str, tokenAddr:str, txHash:str):

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    msgAddr = 'Token: <https://etherscan.io/address/{0}|{1}>'.format(tokenAddr,tokenAddr)
    msgHash = 'Tx Hash: <https://etherscan.io/tx/{0}|{1}>'.format(txHash,txHash)
    
    slack_data = {
        "blocks": 
        [
            {"type": "header","text": {"type": "plain_text","text": "Rug Alert - {0}".format(methodName),"emoji": True}},
            {"type": "section","fields": [{"type": "mrkdwn", "text": msgAddr,}]},
            {"type": "section","fields": [{"type": "mrkdwn", "text": msgHash,}]}
        ]
    }

    data=json.dumps(slack_data)
    resp = requests.post(url, headers=headers, data=data)