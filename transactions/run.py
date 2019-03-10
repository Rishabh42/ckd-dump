import requests
import json
import base64
import time

url = "http://localhost:8383"
rpcuser = "ckrpc"
rpcpassword = "RLK7PkninxV6uvztChFLZR4lwGIHZvwfBpxK6kXAOAo"
walletpassword = "mypassword"
walletaccount = "my_test_account"
fee = 100000
publicKey = "BANyQ50v/jWXz4dKpeXclE21aTgDJhmIgCCNH7sxAzuZqfSx6im19iqZjWRHlbrWh2dQC++aixYT+60a+kq9+Rg="

def request(method, params):
    unencoded_str = rpcuser + ":" + rpcpassword
    encoded_str = base64.b64encode(unencoded_str.encode())
    headers = {
        "content-type": "application/json",
        "Authorization": "Basic " + encoded_str.decode('utf-8')}
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response

# retrieve an output to spend
toSpend = request("listunspentoutputs", {"password": walletpassword, "account": walletaccount})["result"]["outputs"][0]

# input wrapper spending output
input = {"outputId": toSpend["id"]}

# new output for spent funds (minus fee)
newOutput = {"value": toSpend["value"] - fee,
             "nonce": 0,
             "data": {"publicKey": publicKey}}

# the unsigned transaction
transaction = {
    "inputs": [input],
    "outputs": [newOutput],
    "timestamp": int(time.time()),
}
print(json.dumps(transaction, sort_keys=True, indent=4))

# have ckd sign the unsigned transaction for us
signed = request("signtransaction", {"transaction": transaction, "password": walletpassword})["result"]
print(json.dumps(signed, sort_keys=True, indent=4))

# broadcast the signed transaction on the network
success = request("sendrawtransaction", {"transaction": signed})["result"]
print(success)
