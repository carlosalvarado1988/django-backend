import requests


endopoint = "http://localhost:8000/api/products/004212423/"

get_response = requests.get(endopoint)

print(get_response.json())
print(get_response.status_code)
