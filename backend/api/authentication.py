from rest_framework.authentication import TokenAuthentication as BaseTokenAuth

# we add ur custom class
class TokenAuthentication(BaseTokenAuth):
    keyword = 'Bearer'