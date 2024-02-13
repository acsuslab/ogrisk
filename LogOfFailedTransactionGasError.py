from web3 import Web3

# Initialize Web3 with Infura provider
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/89358848da1e4bc9872d0d4400a198d5'))

def get_event_topics(tx_hash):
    try:
        # Get transaction receipt
        receipt = web3.eth.get_transaction_receipt(tx_hash)

        if receipt:
            event_topics = []
            # Iterate through logs
            for log in receipt['logs']:
                if log['topics']:
                    event_topics.append(log['topics'][0])
            return event_topics
        else:
            print("Transaction receipt not found.")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    # Replace 'YOUR_TX_HASH' with the transaction hash you want to check
    tx_hash = '0x9642f3652dbdb01956611e67811183c635c7e2cb9311822240f5bfafc5a36135'
    event_topics = get_event_topics(tx_hash)
    if event_topics:
        print(f"Event topics for transaction {tx_hash}:")
        for topic in event_topics:
            print(topic)
    else:
        print(f"No event topics found for transaction {tx_hash}")
