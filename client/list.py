import requests


endopoint = "http://localhost:8000/api/products/"

get_response = requests.get(endopoint)

print(get_response.json())
print(get_response.status_code)
