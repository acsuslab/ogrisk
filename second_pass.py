import json
import os
import requests
import time
from dotenv import load_dotenv

ETHERSCAN_API_URL = 'https://api.etherscan.io/api'

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv('API_KEY')

#setting up variables for json formatting
data = {}
data['current_contract_index'] = 0
data['open_source_contracts'] = []

#Specify the file path to read the data from and write the data to (will most likely be data.json)
file_path = "data.json"

#checking if there is an existing output file
#if there is then setting the values for the current contract index and the 
if os.path.exists(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    data['current_contract_index'] = data['current_contract_index']
    data['open_source_contracts'] = data['open_source_contracts']

'''
Main program loop, it loops through the addresses in the array that have not been read yet.
For each address in the json file, the function will get the address data, append that address
data to the list for output and then prints to the json file. 
'''
def main():
    for i in range(data['current_contract_index'], len(data['open_source_contracts'])):
        address = data['open_source_contracts'][i]["address"]
        #getting the data for the transactions from the address
        addressData = getAddressData(address)
        if(addressData[0] != 0):
            #adding out of gas txns to the output
            data['open_source_contracts'][data['current_contract_index']] = {"address": address,
                                                                       "total_number_of_txns": addressData[1],
                                                                       "total_number_of_oug_txns": addressData[2],
                                                                       "compiler_version": addressData[3],
                                                                       "maximum_gas_used": addressData[4]}
            data['current_contract_index'] += 1
        else:
            #adding txns to the output that threw an error while calling the API
            data['open_source_contracts'][data['current_contract_index']] = {"address": address,
                                                                       "total_number_of_txns": -1}
            data['current_contract_index'] += 1
        # Write data to the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)

def getTxnData(txnHash):
    params = {
        'module': 'transaction',
        'action': 'getstatus',
        'txhash': txnHash,
        'apikey': API_KEY
    }

    data = construct_api_call(params)

    if data['status'] == '1':
        return data["result"]["errDescription"]
    else:
        print(f"API request error for getting transaction data: {data['result']}\n")
        return "error in getting transaction data"
        
def getCompilerVersion(address):
    params = {
        'module': 'contract',
        'action': 'getsourcecode',
        'address': address,
        'apikey': API_KEY
    }

    data = construct_api_call(params)

    if data['status'] == '1':
        return data['result'][0]['CompilerVersion']
    else:
        print(f"API request error for getting compiler version: {data['result']}\n")
        return "error in getting compiler version"

def getAddressData(address):
    result = []
    num_oog_txn = 0
    total_num_transactions = 0
    startblock = 0
    maximum_gas_used = 0

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

    data = construct_api_call(params)

    if data['status'] == '1':
        #append the status number as the beginning of the list
        result.append(data['status'])
        #get the logs from the api call
        logs = data['result']

        while(True):
            #getting the total number of transactions
            total_num_transactions += len(logs)
            #looping through the transactions to get how many transactions are out of gas & max gas used by a txn
            for txn in logs:
                if(txn['isError'] == "1" and getTxnData(txn['hash']).lower() == "out of gas"):
                    num_oog_txn += 1
                if(int(txn['gasUsed']) >= maximum_gas_used):
                    maximum_gas_used = int(txn['gasUsed'])
            #checking if logs are less than 10000, if they are then break out of loop, if not then get more txns
            if(len(logs) < 10000):
                break
            else:
                #setting the new start block for next iteration
                startblock = logs[len(logs) - 1]['blockNumber']
                params['startblock'] = startblock
                #looping from last transaction to first transaction to remove all transactions that are in the last block
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
        #appending the max gas used to the result
        result.append(maximum_gas_used)
    else:
        print(f"API request error for getting address information: {data['message']}\n")
        #append the status number as the beginning of the list
        result.append(0)
    return result

def construct_api_call(params):
    while(True):
        response = requests.get(ETHERSCAN_API_URL, params=params)
        data = response.json()
        if(data['result'] == 'Max rate limit reached'):
            time.sleep(1)
            continue
        elif (response == '<Response [503]>'):
            time.sleep(1)
            continue
        else:
            break
    return data

#if to run the script
if __name__ == "__main__":
    main()