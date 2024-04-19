import json
import os

ETHERSCAN_API_URL = 'https://api.etherscan.io/api'


# Retrieve the API key from the environment variables
API_KEY = 'NYT56C8D9I25IIKKRE7SJZH15X4CKY68YY'

data = {}
data['current_contract_index'] = 0
data['open_source_contracts'] = []
mainnet_foldernames = []
num_addresses = 0

#!!! change this to whatever filepath the contract folders are held in
smart_contracts_file_path = "/home/maryam/Desktop/Ogrisk/mainnet/"

#!!! change this to whatever file you want the addresses to be written to
file_path = "/home/maryam/Desktop/Ogrisk//data.json"

#getting the foldernames from the mainnet directory
mainnet_foldernames = filtered_files = [file for file in os.listdir(smart_contracts_file_path) if '.' not in file]

#looping through the folders in the mainnet folder
for foldername in mainnet_foldernames:
    #accessing a specific folder in the mainnet file
    with os.scandir(smart_contracts_file_path + "/" + foldername) as it:
        #looping through each file in the folder
        for file in it:
            if file.name.endswith(".sol") and file.is_file():
                split_filename = file.name.split("_")
                address = "0x" + split_filename[0]
                data['open_source_contracts'].append({"address": address})
                num_addresses += 1

# Writing data to the JSON file
with open(file_path, 'w') as json_file:
    json.dump(data, json_file, indent=2)

print(f"Number of addresses added to the json file: {num_addresses}")