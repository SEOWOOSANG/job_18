import requests

response = requests.get("https://www.incruit.com/")
print(response.status_code)