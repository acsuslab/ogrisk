import requests

ETHERSCAN_API_URL = 'https://api.etherscan.io/api'
API_KEY = 'NYT56C8D9I25IIKKRE7SJZH15X4CKY68YY'

def main():

        params = {
            'module': 'account',
            'action': 'txlist',
            'address': '0xB8c77482e45F1F44dE1745F52C74426C631bDD52',
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
            logs = data['result']
            print(logs)
        else:
            print(f"API request error: {data['message']}\n")
            


if __name__ == "__main__":
    main()
