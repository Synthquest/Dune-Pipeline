const { exec, spawn } = require('child_process');
const fs = require('fs');

// Function to read the current hash from the file
function readCurrentHash() {
    return new Promise((resolve, reject) => {
        fs.readFile('current_hash.txt', 'utf8', (err, data) => {
            if (err) {
                return reject(err);
            }
            resolve(data.trim());
        });
    });
}

// Function to run IPFS Kubo daemon and wait for it to be ready
function runIpfsKuboDaemon() {
    return new Promise((resolve, reject) => {
        const daemon = spawn('ipfs', ['daemon']);
        
        daemon.stdout.on('data', (data) => {
            const message = data.toString();
            console.log(message);
            if (message.includes('Daemon is ready')) {
                resolve(daemon);
            }
        });

        daemon.stderr.on('data', (data) => {
            console.error(`Daemon error: ${data}`);
        });

        daemon.on('close', (code) => {
            console.log(`Daemon process exited with code ${code}`);
            reject(new Error('Daemon process exited prematurely'));
        });
    });
}

// Function to publish the hash and record the IPNS name
function publishHash(hash) {
    return new Promise((resolve, reject) => {
        exec(`ipfs name publish /${hash}`, (error, stdout, stderr) => {
            if (error) {
                return reject(`exec error: ${error}`);
            }
            if (stderr) {
                return reject(`stderr: ${stderr}`);
            }

            // Extract the IPNS name from the output
            const match = stdout.match(/Published to (.+):/);
            if (match && match[1]) {
                const ipnsName = match[1];
                // Write the IPNS name to the file
                fs.writeFile('current_ipns.txt', ipnsName, (err) => {
                    if (err) {
                        return reject(`writeFile error: ${err}`);
                    }
                    resolve(stdout.trim());
                });
            } else {
                reject('Failed to extract IPNS name from output');
            }
        });
    });
}

// Main function to orchestrate the process
async function main() {
    let daemon;
    try {
        const hash = await readCurrentHash();
        console.log(`Hash to publish: ${hash}`);
        
        daemon = await runIpfsKuboDaemon();
        console.log('IPFS Kubo daemon is ready.');

        const result = await publishHash(hash);
        console.log(`Publish result: ${result}`);
    } catch (error) {
        console.error(`Error: ${error}`);
    } finally {
        if (daemon) {
            daemon.kill('SIGINT');
            console.log('IPFS Kubo daemon has been stopped.');
        }
    }
}

function withTimeout(promise, timeout) {
    return Promise.race([
        promise,
        new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Operation timed out')), timeout)
        )
    ]);
}

// Set the timeout for the main function to 5 minutes (300000 milliseconds)
withTimeout(main(), 300000).catch(error => {
    console.error(error.message);
});
