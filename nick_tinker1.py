import requests

ETHERSCAN_API_URL = 'https://api.etherscan.io/api'
API_KEY = 'NYT56C8D9I25IIKKRE7SJZH15X4CKY68YY'

def main():

        params = {
            'module': 'transaction',
            'action': 'getstatus',
            'txhash': '0x041276860e9548ba06583bd79372d0aee4b63c6b30878e9c2cddc84e5c055dee',
            'apikey': API_KEY
        }

        response = requests.get(ETHERSCAN_API_URL, params=params)
        data = response.json()

        if data['status'] == '1':
            logs = data['result']
            print(logs)
        else:
            print(f"API request error: {data['message']}\n")
            


if __name__ == "__main__":
    main()
