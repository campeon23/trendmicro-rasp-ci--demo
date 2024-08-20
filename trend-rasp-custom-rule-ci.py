#!/usr/bin/env python3
import requests
import os
import json

# Ensure to export TP_API_KEY='YOURKEY' from the activated venv shell first
TP_API_KEY = str(os.getenv('TP_API_KEY'))

def deployRule(DATA):
    # Base URL and method URL for retrieving group IDs
    BASE_URL = 'https://application.us-1.cloudone.trendmicro.com'
    METHOD_URL = '/accounts/groups'
    API_URL = BASE_URL + METHOD_URL

    # Perform the GET request to retrieve groups
    response = requests.get(API_URL, headers={
        'Authorization': f"ApiKey {TP_API_KEY}"
    })

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve groups: {response.status_code} {response.text}")
        return None

    # Decode the JSON response
    json_response = response.json()

    # Check if the list is empty
    if not json_response:
        print("No groups found. Exiting.")
        return None

    # Extract the group ID
    GROUP_ID = str(json_response[0].get('group_id'))
    print("ENUMERATED GROUP ID: " + GROUP_ID)

    # Update the API URL for deploying the rule
    METHOD_URL = f"/security/rce/{GROUP_ID}/policy"
    API_URL = BASE_URL + METHOD_URL

    # Perform the PUT request to deploy the rule
    response = requests.put(API_URL, json=DATA, headers={
        'Authorization': f"ApiKey {TP_API_KEY}"
    })

    # Print the response status code
    print("Rule deployment response:", response.status_code)
    return response.status_code

# Driver Code
if __name__ == '__main__':
    try:
        with open('example-custom-rasp-rule.json', 'r') as file_handle:
            DATA = json.load(file_handle)

        response = deployRule(DATA)
        if response:
            print(f"Rule deployment response: {response}")
    except FileNotFoundError:
        print("The file 'example-custom-rasp-rule.json' was not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from 'example-custom-rasp-rule.json'.")
