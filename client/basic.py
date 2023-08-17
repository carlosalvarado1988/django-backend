import requests

# endopoint = "https://httpbin.org/status/200"
# endopoint = "https://httpbin.org/anything"
endopoint = "http://localhost:8000"

get_response = requests.get(endopoint, data={"query":"hello world"})
print(get_response.text)
# print(get_response.json())
print(get_response.status_code)