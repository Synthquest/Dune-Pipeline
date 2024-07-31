require('dotenv').config();
const { PINATA_API_KEY, PINATA_SECRET_KEY } = process.env;

// console.log('API Key:', PINATA_API_KEY);
// console.log('Secret Key:', PINATA_SECRET_KEY);

// Use the API keys by providing the strings directly 
const pinataSDK = require('@pinata/sdk');
const pinata = new pinataSDK(PINATA_API_KEY, PINATA_SECRET_KEY);

const fs = require('fs');
const readableStreamForFile = fs.createReadStream('query_results.csv'); // Go up two directory levels

const options = {
    pinataMetadata: {
        name: 'query_results'
    }
};

pinata.pinFileToIPFS(readableStreamForFile, options).then((result) => {
    console.log(result);
}).catch((err) => {
    console.log(err);
});

async function main() {
    try {
        const res = await pinata.testAuthentication();
        console.log(res);
    } catch (error) {
        console.error(error);
    }
}

main();
