import requests
import json

url = "https://backend-production-c33b.up.railway.app/process_games"

payload={}

response = requests.request("POST", url, data=payload)

print(response.text)