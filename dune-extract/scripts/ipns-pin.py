import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def pin_to_ipns(ipfs_hash):
    """
    Pins an IPFS hash to IPNS.

    :param ipfs_hash: The IPFS hash to pin to IPNS.
    :return: The response from the IPFS API.
    """
    # Retrieve the IPFS API, gateway, and IPNS key from environment variables
    ipfs_api = os.getenv('IPFS_API')
    ipfs_gateway = os.getenv('IPFS_GATEWAY')
    ipns_key = os.getenv('IPNS_KEY')

    # Debug statements to check if environment variables are loaded correctly
    print(f"IPFS API: {ipfs_api}")
    print(f"IPFS Gateway: {ipfs_gateway}")
    print(f"IPNS Key: {ipns_key}")

    if not ipfs_api or not ipns_key:
        print("Error: Missing IPFS_API or IPNS_KEY environment variables.")
        return None

    # Define the IPFS API endpoint
    ipfs_api_url = f'{ipfs_api}/api/v0/name/publish'

    # Define the payload
    payload = {
        'arg': ipfs_hash,
        'key': ipns_key,
        'resolve': 'true'
    }

    try:
        # Send the request to the IPFS API
        response = requests.post(ipfs_api_url, params=payload)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Server returned an error: {response.status_code}")
            print(response.json())
            response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return None

# # Example usage
# ipfs_hash = 'QmSiWSoC7qGMSkUz8Gu6so4sgmcL8GyBn7nngguWrUGaSo'  # Replace with your IPFS hash
# result = pin_to_ipns(ipfs_hash)
# print(result)
