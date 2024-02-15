import requests

ETHERSCAN_API_URL = 'https://api.etherscan.io/api'
API_KEY = 'NYT56C8D9I25IIKKRE7SJZH15X4CKY68YY'


def find_out_of_gas_failure():
    page = 1
    while True:
        params = {
            'module': 'logs',
            'action': 'getLogs',
            'fromBlock': '0x0',
            'toBlock': 'latest',
            'status': '1',  # Failed transactions
            'topic0': '0x0000000000000000000000000000000000000000000000000000000000000001',  # Topic for out-of-gas failure
            'page': page,
            'apikey': API_KEY
        }

        response = requests.get(ETHERSCAN_API_URL, params=params)
        data = response.json()

        # Open a file for writing
        with open('out_of_gas_failures.txt', 'a') as f:
            if data['status'] == '1':
                logs = data['result']
                for log in logs:
                    f.write(f"Transaction hash: {log['transactionHash']}, Contract address: {log['address']}\n")
                # If there are more pages, increment page number and continue
                if len(logs) == 1000:
                    page += 1
                else:
                    break
            else:
                f.write(f"API request error: {data['message']}\n")
                break


if __name__ == "__main__":
    find_out_of_gas_failure()
