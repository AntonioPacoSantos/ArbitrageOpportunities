import requests 

BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE,json={"user": "antoniopacosantos11540", "password":"dggybB0#", "account":"REM11540"})

print(response.json())