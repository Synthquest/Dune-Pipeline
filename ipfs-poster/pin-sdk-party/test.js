require('dotenv').config();
const { PINATA_API_KEY, PINATA_SECRET_KEY, PINATA_JWT } = process.env;

console.log('API Key:', PINATA_API_KEY);
console.log('Secret Key:', PINATA_SECRET_KEY);
console.log('JWT:', PINATA_JWT);

const pinataSDK = require('@pinata/sdk');
const pinata = pinataSDK(PINATA_API_KEY, PINATA_SECRET_KEY);

const fs = require('fs');
const path = require('path');

const filePath = path.join('query_results.csv');

async function updateIPFSFile() {
    try {
        // Unpin the existing hash first
        await unpinHash(existingHash);

        // Pin the file to IPFS with the existing hash
        const fetch = await import('node-fetch');
        const readableStreamForFile = fs.createReadStream(filePath);
        const options = {
            pinataMetadata: {
                name: 'query_results'
            }
        };
        const { IpfsHash } = await pinata.pinFileToIPFS(readableStreamForFile, options);
        console.log('File pinned to IPFS with hash:', IpfsHash);

        console.log('Successfully updated IPFS file.');
    } catch (error) {
        console.error('Error updating IPFS file:', error);
    }
}

async function unpinHash(hashToUnpin) {
    try {
        const fetch = await import('node-fetch');
        const response = await fetch.default(`https://api.pinata.cloud/pinning/unpin/${hashToUnpin}`, {
            method: 'DELETE',
            headers: {
                Authorization: `Bearer ${PINATA_JWT}`,
            },
        });
        await response.json(); // Assuming Pinata returns JSON on success
        console.log(`Unpinned hash ${hashToUnpin}`);
    } catch (error) {
        console.error(`Error unpinning hash ${hashToUnpin}:`, error);
        throw error;
    }
}

// Example existing hash
const existingHash = 'QmaU6AyqUt1RjR18yS21LjE5dF663jHehBKw2fyorB8M3C';

updateIPFSFile();
