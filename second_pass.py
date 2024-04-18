import json
import os
import requests
import time
from statistics import mean, stdev


# Constants
ETHERSCAN_API_URL = 'https://api.etherscan.io/api'


# Retrieve the API key from the environment variables
API_KEY = 'NYT56C8D9I25IIKKRE7SJZH15X4CKY68YY'

# File path for data storage
file_path = "/home/maryam/Desktop/Ogrisk/data.json"

# Initialize data structure
data = {'current_contract_index': 0, 'open_source_contracts': []}

# Load existing data if available
if os.path.exists(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

# Main function to process contract addresses
def main():
    for i in range(data['current_contract_index'], len(data['open_source_contracts'])):
        address = data['open_source_contracts'][i]["address"]
        address_data = get_address_data(address)
        if address_data:
            data['open_source_contracts'][i].update(address_data)
            data['current_contract_index'] += 1
            save_data()
        else:
            print(f"No data available for address: {address}")

# Retrieve transaction data for a given transaction hash
def get_txn_data(txn_hash):
    params = {'module': 'transaction', 'action': 'getstatus', 'txhash': txn_hash, 'apikey': API_KEY}
    data = construct_api_call(params)
    if data['status'] == '1':
        return data["result"]["errDescription"]
    else:
        print(f"API request error for getting transaction data: {data['result']}\n")
        return "Error in getting transaction data"

# Retrieve pragma code version for a given contract address
def get_pragma_code_version(address):
    params = {'module': 'contract', 'action': 'getsourcecode', 'address': address, 'apikey': API_KEY}
    data = construct_api_call(params)
    if data['status'] == '1':
        return data['result'][0]['CompilerVersion']
    else:
        print(f"API request error for getting pragma code version: {data['result']}\n")
        return "Error in getting pragma code version"

# Retrieve pragma code for a given contract address
def get_pragma_code(address):
    params = {'module': 'contract', 'action': 'getsourcecode', 'address': address, 'apikey': API_KEY}
    data = construct_api_call(params)
    if data['status'] == '1':
        return data['result'][0]['SourceCode']
    else:
        print(f"API request error for getting pragma code: {data['result']}\n")
        return "Error in getting pragma code"



# Calculate the percentage variation in gas consumption by function (methodID) for each smart contract
def calculate_gas_caps(data):
    gas_caps = {}

    for txn in data['result']:
        method_id = txn['input'][:10]  # first 4 bytes (8 hexadecimal characters or 10 characters if including the '0x' prefix) of the input data.
        gas_used = int(txn['gasUsed'])
        if txn['isError'] == "0":  # Only considering successful transactions
            if method_id not in gas_caps:
                gas_caps[method_id] = [gas_used]
            else:
                gas_caps[method_id].append(gas_used)

    caps_results = {}
    for method_id, gas_list in gas_caps.items():
        if len(gas_list) > 1:
            max_gas = max(gas_list)
            min_gas = min(gas_list)
            percentage_variation = ((max_gas - min_gas) / 30000000)   # Normalize by block gas limit
        else:
            percentage_variation = 0
        caps_results[method_id] = round(percentage_variation, 10)

    return caps_results


# Calculate the standard deviation in gas consumption by function (methodID) for each smart contract
def calculate_gas_std_dev(data):
    gas_std_dev = {}
    for txn in data['result']:
        method_id = txn['input'][:10]  # first 4 bytes (8 hexadecimal characters or 10 characters if including the '0x' prefix) of the input data.
        gas_used = int(txn['gasUsed'])
        if txn['isError'] == "0":  # Only considering successful transactions
            if method_id not in gas_std_dev:
                gas_std_dev[method_id] = [gas_used]
            else:
                gas_std_dev[method_id].append(gas_used)

    std_dev_results = {}
    for method_id, gas_list in gas_std_dev.items():
        if len(gas_list) > 1:
            standard_deviation = stdev(gas_list)
            normalized_std_dev = (standard_deviation / 30000000)  # Normalize by block gas limit
        else:
            normalized_std_dev = 0
        std_dev_results[method_id] = round(normalized_std_dev, 10)

    return std_dev_results


# Retrieve the maximum gas consumed by all transactions
def get_max_gas_used_all(data):
    all_transactions_gas = [int(txn['gasUsed']) for txn in data['result']]
    return round(max(all_transactions_gas) if all_transactions_gas else 0, 4)

# Retrieve the maximum gas consumed by a transaction that ran out of gas in a contract
def get_max_gas_used_oog(data):
    oog_transactions_gas = [int(txn['gasUsed']) for txn in data['result'] if txn['isError'] == "1" and get_txn_data(txn['hash']).lower() == "out of gas"]
    return round(max(oog_transactions_gas) if oog_transactions_gas else 0, 4)

# Retrieve address data including transaction details
def get_address_data(address):
    result = {}
    try:
        params = {'module': 'account', 'action': 'txlist', 'address': address, 'startblock': 0, 'endblock': 99999999,
                  'page': 1, 'offset': 0, 'sort': 'asc', 'apikey': API_KEY}
        data = construct_api_call(params)
        if data['status'] == '1':
            result['total_transactions'] = len(data['result'])
            result['total_failed_transactions'] = sum(1 for txn in data['result'] if txn['isError'] == "1")
            result['total_oog_transactions'] = sum(1 for txn in data['result'] if txn['isError'] == "1" and get_txn_data(txn['hash']).lower() == "out of gas")
            result['maximum_gas_used_all'] = get_max_gas_used_all(data)
            result['maximum_gas_used_oog'] = get_max_gas_used_oog(data)
            result['gas_caps'] = calculate_gas_caps(data)
            result['gas_std_dev'] = calculate_gas_std_dev(data)
            result['average_gas_per_contract'] = round(mean(int(txn['gasUsed']) for txn in data['result']) if result['total_transactions'] > 0 else 0, 4)
            result['pragma_code_version'] = get_pragma_code_version(address)
        else:
            print(f"API request error for address {address}: {data['message']}\n")
            return None
    except Exception as e:
        print(f"Error retrieving data for address {address}: {str(e)}")
        return None
    return result

# Make API call with error handling and rate limiting
def construct_api_call(params):
    while True:
        response = requests.get(ETHERSCAN_API_URL, params=params)
        data = response.json()
        if data['result'] == 'Max rate limit reached' or response.status_code == 503:
            time.sleep(1)
            continue
        else:
            break
    return data

# Save data to file
def save_data():
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

# Count contracts with non-zero out-of-gas transactions
def count_contracts_with_oog_transactions():
    count = sum(1 for contract in data['open_source_contracts'] if contract.get('total_oog_transactions', 0) > 0)
    print(f"Number of contracts with non-zero out-of-gas transactions: {count}")

# Entry point of the script
if __name__ == "__main__":
    main()
    count_contracts_with_oog_transactions()