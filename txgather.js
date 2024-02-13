import fetch from "node-fetch";
import Web3 from "web3";
import net from "net";
import * as os from "os";
import * as fs from "fs";
import assert from "assert";

async function get_last_tx_from_address(address) {
    try {
        const response = await fetch(`https://api-ropsten.etherscan.io/api?module=account&action=txlist&address=${address}&startblock=0&endblock=99999999&sort=desc&apikey=8TUK1TGEP6Z9MTMTKQYN97DPKNCR876B6A`);
        const json = await response.json();

        //console.log(JSON.stringify(json));

        if(json.status !== "1" || json.message !== "OK") {
            return {}
        }

        if(json.result.length >= 1) {
            return json.result[0];
        }
        // let address_lowercase = address.toLowerCase();
        // for(let x of json.result) {
        //     //console.log(`TXN: ${JSON.stringify(x)}`);
        //     if(x.from.toLowerCase() === address_lowercase) {
        //         return x;
        //     }
        // }
        //
        // return {};
    } catch (error) {
        console.log(`ERROR: ${error.message}`);
        return {};
    }
}

function serializeTx(block, tx) {
    return `${tx.blockNumber}:${block.timestamp}:${tx.hash}:${tx.nonce}:${tx.blockHash}:${tx.transactionIndex}:${tx.from}:${tx.to}:${tx.value}:${tx.gas}:${tx.gasPrice}`;
}

function deserializeTx(serializedTx) {
    let fields = serializedTx.split(":");
    assert(fields.length === 11);

    let tx = {
        blockNumber: fields[0],
        blockTimestamp: fields[1],
        hash: fields[2],
        nonce: fields[3],
        blockHash: fields[4],
        transactionIndex: fields[5],
        from: fields[6],
        to: fields[7],
        value: fields[8],
        gas: fields[9],
        gasPrice: fields[10]
    };

    return tx;
}

async function main() {
    // const home_dir = os.homedir();
    // if(process.argv.length !== 3) {
    //     console.log("ERROR: Expected one argument.");
    //     console.log("USAGE: node txsea <TRANSACTION_ID>");
    //     process.exit(1);
    // }
// "0xfb564b3FA584837a26623Aa1FfC83027Be2B93A4"

    //const Web3 = require('web3');
    //var net = require('net');
    var web3 = new Web3('/home/nick/mainnet/geth.ipc', net);
    //var web3 = new Web3('ws://35.9.42.185:8547');
    //let web3 = new Web3("wss://mainnet.infura.io/ws/v3/ef1ce1202d8248a69d1eacd3a6237f28");

    for(let round = 0; round <= 13; round++) {
        let start_block = round * 1000000;
        let end_block = round < 13 ? (round+1) * 1000000 - 1 : 13550719;
        let filepath = `/home/nick/transactions-round-${round}.txt`;

        for(let i = start_block; i <= end_block; i++) {
            let res1 = await web3.eth.getBlock(i);

            console.log(`ROUND ${round}, processing block: ${i}`);

            if (res1.transactions.length === 0) {
                console.log(`Block ${i} has no transactions.`);
            } else {
                console.log(`Block ${i} has ${res1.transactions.length} transactions.`);
            }

            for (let x of res1.transactions) {
                let res2 = await web3.eth.getTransaction(x);

                fs.appendFileSync(filepath, (serializeTx(res1, res2) + "\n"), (err) => {
                    if (err) {
                        console.log("File writing error.");
                        process.exit(1);
                    }
                });
            }
        }
    }

    // for(let i = 0; i < 13550719; i++) {
    //     let res1 = await web3.eth.getBlock(i);
    //
    //     console.log(`Processing block: ${i}`);
    //
    //     if(res1.transactions.length === 0) {
    //         console.log(`Block ${i} has no transactions.`);
    //     } else {
    //         console.log(`Block ${i} has ${res1.transactions.length} transactions.`);
    //     }
    //
    //     // console.log(`BLOCK: ${JSON.stringify(res1)}`);
    //
    //     for(let x of res1.transactions) {
    //         //console.log(`X: ${x}`);
    //         let res2 = await web3.eth.getTransaction(x);
    //         //console.log(`HASH: ${res2.hash}`);
    //
    //         fs.appendFileSync("/home/nick/transactions.txt", (serializeTx(res1, res2) + "\n"), (err) => {
    //             if(err) {
    //                 console.log("File writing error.");
    //                 process.exit(1);
    //             }
    //         });
    //     }
    // }

    process.exit(0);
}

main();
