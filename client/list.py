import requests


endopoint = "http://localhost:8000/api/products/"

get_response = requests.get(endopoint)

print(get_response.json())
print(f"status: {get_response.status_code}")
