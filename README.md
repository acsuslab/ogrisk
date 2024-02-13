# ogrisk
OGRisk - Out-of-Gas Risk Estimator

AllFailed.py and its txt file 'failed-transactions.txt' are useless, but it has an attempt to do what the name says (from Infura's API).

What's in the 'out_of_gas_failures.txt' belongs to the OutOfGasFailures.py, and what's in it is not really failed transactions (from Etherscan's API).

GetSourceCode.py takes the transactions and contracts from 'out_of_gas_failures.txt' and merges everything and counts to 'contract_counts.txt' (from Etherscan's API).

LogOfFailedTransactionGasError.py gets you the receipt information from a transaction, for a transaction hash (from Etherscan's API).

nick_tinker2.py illustrates how to get the list of transactions for a given smart contracts, including failed transactions (from Etherscan's API). 

nick_tinker1.py illustrates how to get the "out-of-gas" status of a given transaction using transaction hash (from Etherscan's API).

TopicNumber.py tries to test for all possible combinations of topic numbers to match the topic number of that failed transaction hash (from Etherscan's API).

Txgather.js gets the last transaction for a contract in the blockchain, and iterates through millions of them using a node. It then print this information from Ethereum's API: Block number, Block timestamp, Transaction hash, Nonce, Block hash, Transaction index, Sender address (from), Receiver address (to), Transaction value, Gas used, Gas price
