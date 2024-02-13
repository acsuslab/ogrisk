import requests
import pytest

@pytest.fixture
def topic_number():
    # Define your fixture data here
    return '0x0000000000000000000000000000000000000000000000000000000000000000'

def test_topic_number(topic_number):
    # Your test code using the 'topic_number' fixture goes here
    assert len(topic_number) == 66  # Example assertion
    print(f"Topic number passed: {topic_number}")

ETHERSCAN_API_URL = 'https://api.etherscan.io/api'
API_KEY = 'NYT56C8D9I25IIKKRE7SJZH15X4CKY68YY'
TARGET_TRANSACTION_HASH = '0x041276860e9548ba06583bd79372d0aee4b63c6b30878e9c2cddc84e5c055dee'

def test_topic_number(topic_number):
    page = 1
    while True:
        params = {
            'module': 'logs',
            'action': 'getLogs',
            'fromBlock': '0x0',
            'toBlock': 'latest',
            'status': '0',  # Failed transactions
            'topic0': topic_number,  # Topic for out-of-gas failure
            'page': page,
            'apikey': API_KEY
        }

        response = requests.get(ETHERSCAN_API_URL, params=params)
        data = response.json()

        response = requests.get(ETHERSCAN_API_URL, params=params)
        data = response.json()

        if data['status'] == '1':
            logs = data['result']
            for log in logs:
                if log['transactionHash'].lower() == TARGET_TRANSACTION_HASH.lower():
                    print(f"Match found! Topic number: {topic_number}")
                    with open('TopicNumb.txt', 'w') as f:
                        f.write(topic_number)
                    return True
            # If there are more pages, increment page number and continue
            if len(logs) == 1000:
                page += 1
            else:
                break
        else:
            print(f"API request error: {data['message']}")
            break


def find_out_of_gas_failure():
    for i in range(2**256):  # Iterate through all possible topic numbers
        topic_number = hex(i)
        print(f"Testing topic number: {topic_number}")
        if test_topic_number(topic_number):
            break  # Stop iterating if a match is found

if __name__ == "__main__":
    find_out_of_gas_failure()
