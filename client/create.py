import requests


endopoint = "http://localhost:8000/api/products/"
 
data = {
    "title": "product 22",
    "price": 22
}
get_response = requests.post(endopoint, json=data)

print(get_response.json())
print(f"status: {get_response.status_code}")
