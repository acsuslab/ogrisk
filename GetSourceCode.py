import requests

ETHERSCAN_API_URL = 'https://api.etherscan.io/api'
API_KEY = 'NYT56C8D9I25IIKKRE7SJZH15X4CKY68YY'


def get_contract_info(contract_address):
    params = {
        'module': 'contract',
        'action': 'getsourcecode',
        'address': contract_address,
        'apikey': API_KEY
    }

    response = requests.get(ETHERSCAN_API_URL, params=params)
    data = response.json()

    if data['status'] == '1' and data['message'] == 'OK':
        result = data['result'][0]  # Assuming only one result is returned
        source_code = result['SourceCode']
        return True, source_code
    else:
        return False, None


def process_out_of_gas_failures():
    # Open a file for writing logs
    count_file = open('contract_counts.txt', 'w')

    # Read transaction hashes and contract addresses from file
    with open('out_of_gas_failures.txt', 'r') as f:
        lines = f.readlines()

    # Maintain a dictionary to keep track of the count of failed transactions for each contract
    contract_counts = {}

    # Maintain a dictionary to store transaction hashes for each contract
    contract_transactions = {}

    # Process each line to get transaction hash and contract address
    for line in lines:
        transaction_hash, contract_address = line.strip().split(", ")

        # Update the count for the current contract
        contract_counts[contract_address] = contract_counts.get(contract_address, 0) + 1

        # Add transaction hash to the list of transactions for the current contract
        if contract_address in contract_transactions:
            contract_transactions[contract_address].append(transaction_hash)
        else:
            contract_transactions[contract_address] = [transaction_hash]

        # Check if contract is verified and get source code
        is_verified, source_code = get_contract_info(contract_address)

        # Write contract count and associated transaction hashes to the count file
        count_file.write(
            f"Contract Address: {contract_address} (Associated with {contract_counts[contract_address]} failed transactions)\n")
        count_file.write(f"Verified: {'Yes' if is_verified else 'No'}\n")

        if is_verified:
            count_file.write("Source Code:\n")
            count_file.write(source_code)
        else:
            count_file.write("Source code not available or not verified.\n")

        count_file.write("Transaction Hashes:\n")
        count_file.write("\n".join(contract_transactions[contract_address]))
        count_file.write("\n\n")

    # Close the count file after processing all logs
    count_file.close()


if __name__ == "__main__":
    process_out_of_gas_failures()
