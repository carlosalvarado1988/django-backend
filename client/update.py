import requests

endpoint = "http://localhost:8000/api/products/1/update/"
 
data = {
    "title": "product updated 3",
    "price": 221
}

get_response = requests.put(endpoint, json=data)
print(get_response.json())
print(f"status: {get_response.status_code}")