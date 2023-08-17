import requests

# endopoint = "https://httpbin.org/status/200"
# endopoint = "https://httpbin.org/anything"
endopoint = "http://localhost:8000/api"

get_response = requests.post(endopoint, params={"abc": 123}, json={"title": 'ABC', "other": "Product 1", "price":10})
print(get_response.headers)
# print(get_response.text)

print(get_response.json())
print(get_response.status_code)
# print(get_response.json()["message"])