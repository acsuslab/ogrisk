import json
import os
import requests
from dotenv import load_dotenv

ETHERSCAN_API_URL = 'https://api.etherscan.io/api'

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv('API_KEY')

data = {}
data["open_source_contracts"] = []

def getTxnData(txnHash):

        params = {
            'module': 'transaction',
            'action': 'getstatus',
            'txhash': txnHash,
            'apikey': API_KEY
        }

        response = requests.get(ETHERSCAN_API_URL, params=params)
        data = response.json()

        if data['status'] == '1':
            return data["result"]["errDescription"]
        else:
            return(f"API request error: {data['message']}\n")
        
def getCompilerVersion(address):
    params = {
        'module': 'contract',
        'action': 'getsourcecode',
        'address': address,
        'apikey': API_KEY
    }

    response = requests.get(ETHERSCAN_API_URL, params=params)
    data = response.json()

    if data['status'] == '1':
        return data['result'][0]['CompilerVersion']
    else:
        return(f"API request error: {data['message']}\n")

def getAddressData(address):
    result = []
    page = 1
    num_oog_txn = 0

    params = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': 0,
        'endblock': 99999999,
        'page': page,
        'offset': 0,
        'sort': 'asc',
        'apikey': API_KEY
    }

    while(True):
        response = requests.get(ETHERSCAN_API_URL, params=params)
        data = response.json()
        if(response != '<Response [503]>'):
            break

    if data['status'] == '1':
        #append the status number as the beginning of the list
        result.append(data['status'])
        #get the logs from the api call
        logs = data['result']
        #Append the total number of transactions to the result
        result.append(len(logs))
        if(len(logs) > 0):
            #looping through the transactions to get how many transactions are out of gas
            num_oog_txn = 0
            for txn in logs:
                if(txn['isError'] == "1" and getTxnData(txn['hash']).lower() == "out of gas"):
                    num_oog_txn += 1
            #appending the number of out of gas transactions to the result
            result.append(num_oog_txn)
            #appending the compiler version to the result
            result.append(getCompilerVersion(address))
    else:
        print(f"API request error: {data['message']}\n")
        #append the status number as the beginning of the list
        result.append(0)
    return result

#!!!only getting from test folder
with os.scandir("/Volumes/External-Storage/smart-contract-sanctuary-ethereum/contracts/test3") as it:
    for entry in it:
        if entry.name.endswith(".sol") and entry.is_file():
            split_filename = entry.name.split("_")
            address = "0x" + split_filename[0]
            #getting the data for the transactions from the address
            addressData = getAddressData(address)
            #checking if there was an error in the api call
            #if(addressData[0] == 0 or addressData[2] == 0):
                #data["open_source_contracts"].append({"address": address})
            if(addressData[0] != 0 and addressData[2] != 0):
                data["open_source_contracts"].append({"address": address,
                                                    "total_number_of_txns": addressData[1],
                                                    "total_number_of_oug_txns": addressData[2],
                                                    "compiler version": addressData[3]})


#Writing to the JSON file
            
# Specify the file path
file_path = "data-test.json"

# Write data to the JSON file
with open(file_path, 'w') as json_file:
    json.dump(data, json_file, indent=2)