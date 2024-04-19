import json
import os
import requests


ETHERSCAN_API_URL = 'https://api.etherscan.io/api'

<<<<<<< HEAD
=======
# Load environment variables from the .env file

>>>>>>> eb52bfc (ACSUS Lab)

# Retrieve the API key from the environment variables
API_KEY = 'NYT56C8D9I25IIKKRE7SJZH15X4CKY68YY'

data = {}
data['current_contract_index'] = 0
data['open_source_contracts'] = []

#Specify the file path to write the data to
file_path = "data-test.json"

#checking if there is an exisiting output file
if os.path.exists(file_path):
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)
    data['current_contract_index'] = existing_data['current_contract_index']
    data['open_source_contracts'] = existing_data['open_source_contracts']

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
    num_oog_txn = 0
    total_num_transactions = 0
    startblock = 0

    params = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': startblock,
        'endblock': 99999999,
        'page': 1,
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

        while(True):
            #getting the total number of transactions
            total_num_transactions += len(logs)
            #looping through the transactions to get how many transactions are out of gas
            for txn in logs:
                if(txn['isError'] == "1" and getTxnData(txn['hash']).lower() == "out of gas"):
                    num_oog_txn += 1
            #checking if logs are less than 10000, if they are then break out of loop, if not then get more txns
            if(len(logs) < 10000):
                break
            else:
                #setting the new start block for next iteration
                startblock = logs[len(logs) - 1]['blockNumber']
                params['startblock'] = startblock
                #looping from last transaction to first transaction
                #to remove all transactions that are in the last block
                i = 0
                while(logs[(len(logs) - 1) - i]['blockNumber'] == startblock):
                    if(logs[(len(logs) - 1) - i]['blockNumber'] == startblock):
                        total_num_transactions -= 1
                        if(logs[(len(logs) - 1) - i]['isError'] == "1" and 
                            getTxnData(logs[(len(logs) - 1) - i]['hash']).lower() == "out of gas"):
                            num_oog_txn -= 1
                    i += 1
                response = requests.get(ETHERSCAN_API_URL, params=params)
                data = response.json()
                logs = data['result']
        #Append the total number of transactions to the result
        result.append(total_num_transactions)
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
with os.scandir("/Users/user/Desktop/Rowan PhD Data Science/Spring 2024/CS 07556_Machine Learning 1/Paper project/smart-contract-sanctuary-ethereum-master/contracts/mainnet/00") as it:
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
                data['open_source_contracts'].append({"address": address,
                                                    "total_number_of_txns": addressData[1],
                                                    "total_number_of_oug_txns": addressData[2],
                                                    "compiler version": addressData[3]})
                data['current_contract_index'] += 1
            else:
                data['open_source_contracts'].append({"address": address,
                                                    "total_number_of_txns": -1})
                data['current_contract_index'] += 1
        # Write data to the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)