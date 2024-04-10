const parser = require('@solidity-parser/parser')
const fs = require('fs');

if (process.argv.length > 2) {
  const filepath = process.argv[2];

  try {
    const input = fs.readFileSync(filepath, { encoding: 'utf8' });
    
    try {
      const ast = parser.parse(input)
      console.log(JSON.stringify(ast, null, 2))
    } catch (e) {
      if (e instanceof parser.ParserError) {
        console.error(e.errors)
      }
    }
  } catch (error) {
    console.error('Error reading the file:', error);
  }
} else {
  console.log('Error: No argument provided. Please provide an argument.');
}






// const input = `
//     import './hello.sol';

//     contract test {
//         uint256 a;
//         function f() {}
//     }
// `
