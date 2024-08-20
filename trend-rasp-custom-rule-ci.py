#!/usr/bin/env python3
import requests, os, json
#be sure to do export TP_API_KEY='YOURKEY' from venv activated shell first
TP_API_KEY = str(os.getenv('TP_API_KEY'))


def deployRule(DATA):
  #for testing example purposes to enumerate the group UID
  #example kv pair 'group_id': 'f1c6464c-d506-4612-b33c-99999999'
  BASE_URL = 'https://application.us-1.cloudone.trendmicro.com'
  METHOD_URL = '/accounts/groups'
  API_URL = BASE_URL + METHOD_URL

  response = requests.get(API_URL, headers= {
      'Authorization' : "ApiKey " + TP_API_KEY
  })
#   #returns as bytes for some reason. need to convert to enum
#   json_response = json.loads(response.content.decode())
#   GROUP_ID = str(json_response[0]['group_id'])
#   print("ENUMERATED GROUP ID: " + GROUP_ID)
#   #just resuse the same variables since its procedural and not iterative
#   METHOD_URL = "/security/rce/" + GROUP_ID + "/policy"
#   API_URL = BASE_URL + METHOD_URL

#   response = requests.put(API_URL, json=DATA, headers= {
#       'Authorization' : "ApiKey " + TP_API_KEY})
#   #openAPI spec nothiong is returned other than a 2XX
#   #see https://cloudone.trendmicro.com/docs/application-security/api-reference/tag/open_api#paths/~1security~1rce~1%7Bgroup_id%7D~1policy/put
#   #print(response.status_code)
#   return response.status_code


# # Driver Code 
# if __name__ == '__main__':
#   file_handle = open('example-custom-rasp-rule.json', 'r')
#   DATA = json.load(file_handle)
#   response = deployRule(DATA)
#   print(response)

#   response = requests.get(API_URL, headers={
#       'Authorization': "ApiKey " + TP_API_KEY
#   })

  if response.status_code != 200:
      print(f"Failed to retrieve groups: {response.status_code} {response.text}")
      return None

  # Decode the JSON response
  json_response = json.loads(response.content.decode())

  if not json_response:  # Check if the list is empty
      print("No groups found. Exiting.")
      return None

  GROUP_ID = str(json_response[0].get('group_id'))
  print("ENUMERATED GROUP ID: " + GROUP_ID)

  # Reuse the same variables since it's procedural and not iterative
  METHOD_URL = f"/security/rce/{GROUP_ID}/policy"
  API_URL = BASE_URL + METHOD_URL

  response = requests.put(API_URL, json=DATA, headers={
      'Authorization': "ApiKey " + TP_API_KEY
  })

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
