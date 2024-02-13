import requests

INFURA_API_URL = 'https://mainnet.infura.io/v3/89358848da1e4bc9872d0d4400a198d5'

def get_failed_transactions():
    failed_txs = []

    # Specify the filter object
    filter_params = {
        'fromBlock': '0x46523C',
        'toBlock': '0x46DF5B',
        'topics': ['0x241ea03ca20251805084d27d4440371c34a0b85ff108f6bb5611248f73818b80']
        # Add more filter parameters as needed
    }

    # Construct the request payload
    payload = {
        'jsonrpc': '2.0',
        'method': 'eth_getLogs',
        'params': [filter_params],
        'id': 1
    }

    # Define headers with authentication token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR-API-TOKEN'
    }

    # Make the HTTP POST request with headers
    response = requests.post(INFURA_API_URL, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if 'result' in data:
            logs = data['result']
            for log in logs:
                # Extract relevant information from the log
                tx_hash = log['transactionHash']
                # Add the transaction hash to the list of failed transactions
                failed_txs.append(tx_hash)
        else:
            print(f"Error: {data['error']['message']}")
    else:
        print(f"HTTP request failed with status code {response.status_code}")

    return failed_txs

if __name__ == "__main__":
    failed_transactions = get_failed_transactions()
    with open('failed_transactions.txt', 'w') as f:
        for tx_hash in failed_transactions:
            f.write(f"{tx_hash}\n")
