const solc = require('solc');
const fs = require('fs');

// Read the Solidity source code
const contractCode = fs.readFileSync('Sample.sol', 'utf8');

// Define the input for the Solidity compiler
const input = {
    language: 'Solidity',
    sources: {
        'Sample.sol': {
            content: contractCode,
        },
    },
    settings: {
        outputSelection: {
            '*': {
                '*': ['*'],
            },
        },
    },
};

// Compile the contract
const output = JSON.parse(solc.compile(JSON.stringify(input)));

// Check if there were any compilation errors
if (output.errors) {
    console.error('Compilation errors occurred:');
    output.errors.forEach(error => console.error(error.formattedMessage));
    process.exit(1); // Exit the script with a non-zero exit code
}

// Extract the AST from the output
const contractName = 'stakingContract'; // Change this to match your contract name
const contractAST = output.contracts['Sample.sol'][contractName];

// Check if contractAST is defined and has the 'ast' property
if (contractAST && contractAST.ast) {
    // Print the AST in JSON format
    console.log(JSON.stringify(contractAST.ast, null, 2));
} else {
    console.error('Failed to generate AST for the contract.');
}
