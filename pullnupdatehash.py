import subprocess
import os
import time
import re

def run_data_pull_script():
    """Run the dataPull.py script."""
    print("Running dataPull.py...")
    subprocess.run(['python', os.path.join('dune-extract', 'scripts', 'dataPull.py')], check=True)
    print("dataPull.py has finished executing.")

def wait_for_csv_update(file_path, timeout=300, check_interval=5, stable_interval=10):
    """Wait for the query_results.csv file to finish updating."""
    print(f"Waiting for {file_path} to finish updating...")
    start_time = time.time()
    last_size = -1
    stable_time = 0
    
    while time.time() - start_time < timeout:
        if os.path.exists(file_path):
            current_size = os.path.getsize(file_path)
            if current_size != last_size:
                last_size = current_size
                stable_time = time.time()
            elif time.time() - stable_time >= stable_interval:
                print(f"{file_path} is stable and ready.")
                return True
        time.sleep(check_interval)
    
    print(f"Timeout: {file_path} was not updated within {timeout} seconds.")
    return False

def run_node_script(script_path):
    """Run the index.js script using Node.js and return its output."""
    print(f"Running {script_path}...")
    result = subprocess.run(['node', script_path], capture_output=True, text=True, check=True)
    print(f"{script_path} has finished executing.")
    return result.stdout.strip()

def extract_ipfs_hash(script_output):
    """Extract the IPFS hash from the script output."""
    # Match the IPFS hash using regex
    match = re.search(r"IpfsHash: '([^']+)'", script_output)
    if match:
        return match.group(1)
    else:
        raise ValueError("IPFS hash not found in the script output.")

def write_to_file(file_path, content):
    """Write the given content to the specified file, overwriting any existing content."""
    # Open the file in write mode to clear its contents before writing new content
    with open(file_path, 'w') as file:
        file.write(content)

if __name__ == '__main__':
    data_pull_script_path = os.path.join('dune-extract', 'scripts', 'dataPull.py')
    csv_file_path = 'query_results.csv'
    node_script_path = os.path.join('ipfs-poster', 'pin-sdk-party', 'index.js')
    current_hash_file_path = 'current_hash.txt'

    try:
        run_data_pull_script()
        if wait_for_csv_update(csv_file_path):
            script_output = run_node_script(node_script_path)
            ipfs_hash = extract_ipfs_hash(script_output)
            write_to_file(current_hash_file_path, ipfs_hash)
            print(f"IPFS hash {ipfs_hash} written to {current_hash_file_path}.")
        else:
            print("CSV file did not update correctly. Exiting.")
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"An error occurred: {e}")
