#!/usr/bin/env python3
import requests
import os
import json
import sys

# Constants
BASE_URL = 'https://application.us-1.cloudone.trendmicro.com'
GROUPS_ENDPOINT = '/accounts/groups'
RCE_POLICY_ENDPOINT = '/security/rce/{group_id}/policy'

# Ensure API key is set
TP_API_KEY = os.getenv('TP_API_KEY')
if not TP_API_KEY:
    print("Error: TP_API_KEY environment variable is not set.")
    sys.exit(1)

def get_group_id():
    """Retrieve the first group ID from the API."""
    url = BASE_URL + GROUPS_ENDPOINT
    try:
        response = requests.get(url, headers={'Authorization': f"ApiKey {TP_API_KEY}"})
        print(f"Response status code GET: {response.status_code}")
        response.raise_for_status()
        groups = response.json()
        
        if not groups:
            print("No groups found.")
            return None
        
        group_id = groups[0].get('group_id')
        if not group_id:
            print("Group ID not found in the response.")
            return None

        print(f"Enumerated Group ID: {group_id}")
        return group_id
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve group ID: {e}")
        return None

def deploy_rule(group_id, data):
    """Deploy a custom RASP rule to the specified group."""
    url = BASE_URL + RCE_POLICY_ENDPOINT.format(group_id=group_id)
    try:
        response = requests.put(url, json=data, headers={'Authorization': f"ApiKey {TP_API_KEY}"})
        print(f"Rule deployment response: {response.status_code}")
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Failed to deploy rule: {e}")
        return None

def main():
    """Main function to deploy the RASP rule."""
    try:
        with open('example-custom-rasp-rule.json', 'r') as file_handle:
            data = json.load(file_handle)
    except FileNotFoundError:
        print("The file 'example-custom-rasp-rule.json' was not found.")
        return
    except json.JSONDecodeError:
        print("Error decoding JSON from 'example-custom-rasp-rule.json'.")
        return

    group_id = get_group_id()
    if group_id:
        deploy_rule(group_id, data)

if __name__ == '__main__':
    main()
