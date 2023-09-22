import requests
from getpass import getpass




# adaptjng api call to use auth token.
# first step to get the auth token
get_auth_token_endopoint = "http://localhost:8000/api/auth/"
# make sure to not send raw passwords
username = input("What is your username\n")
password = getpass("What is your password\n") #allow to input the password in the console // sept2023
get_auth_token_response = requests.post(get_auth_token_endopoint, json={'username': 'staff', 'password': password})

print('get_auth_token_response', get_auth_token_response.json())
print(f"status: {get_auth_token_response.status_code}")


if get_auth_token_response.status_code == 200:
    endopoint = "http://localhost:8000/api/products/"
    token = get_auth_token_response.json()['token']
    headers = {
        # "Authorization": f"Token {token}" # using the built-in authentication_classes -> authentication.TokenAuthentication
        "Authorization": f"Bearer {token}" # using the custom authentication_classes -> TokenAuthentication
    }
    get_response = requests.get(endopoint, headers=headers)

    print(get_response.json())
    print(f"status: {get_response.status_code}")