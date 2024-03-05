const fs = require('fs');
const parser = require('@solidity-parser/parser');

// Read the Solidity file
const CONTRACT_FILE = '00CCc5Fe33fa66847082af413d4A8700cd7CDe16_Rug.sol';
const content = fs.readFileSync(CONTRACT_FILE).toString();

// Parse the Solidity code into an AST
try {
    const ast = parser.parse(content);

    // Write the AST to a JSON file
    const jsonOutput = JSON.stringify(ast, null, 2); // Pretty-printed JSON with 2 spaces indentation
    fs.writeFileSync('ast_output.json', jsonOutput);

    console.log('AST successfully written to ast_output.json');

} catch (error) {
    console.error('Error parsing Solidity file:', error.message);
    if (error instanceof parser.ParserError) {
        console.error('Syntax Errors:', error.errors);
    }
}
