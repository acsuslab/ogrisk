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

def get_txn_data(address):
    result = []

    params = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': 0,
        'endblock': 99999999,
        'page': 1,
        'offset': 0,
        'sort': 'asc',
        'apikey': API_KEY
    }

    response = requests.get(ETHERSCAN_API_URL, params=params)
    data = response.json()

    if data['status'] == '1':
        #Append the error status to the result
        result.append(True)
        #get the logs from the api call
        logs = data['result']
        #Append the total number of transactions to the result
        result.append(len(logs))
        #looping through the transactions to get how many transactions are out of gas
        num_oog_txn = 0
        for txn in logs:
            if(txn['isError'] == "1"):
                num_oog_txn += 1
        #appending the number of out of gas transactions to the result
        result.append(num_oog_txn)
    else:
        print(f"API request error: {data['message']}\n")
        result.append(False)
    return result

#!!!only getting from first folder in the mainnet contracts
with os.scandir("/Volumes/External-Storage/smart-contract-sanctuary-ethereum/contracts/mainnet/00") as it:
    for entry in it:
        if entry.name.endswith(".sol") and entry.is_file():
            split_filename = entry.name.split("_")
            address = "0x" + split_filename[0]
            #getting the data for the transactions from the address
            txn_data = get_txn_data(address)
            if(txn_data[0] == False):
                data["open_source_contracts"].append({"address": address,
                                                    "error": txn_data[0]})
            else:
                data["open_source_contracts"].append({"address": address,
                                                    "error": txn_data[0],
                                                    "total_number_of_txns": txn_data[1],
                                                    "total_number_of_oug_txns": txn_data[2]})
            #print("0x" + split_filename[0])


#Writing to the JSON file
            
# Specify the file path
file_path = "data.json"

# Write data to the JSON file
with open(file_path, 'w') as json_file:
    json.dump(data, json_file, indent=2)