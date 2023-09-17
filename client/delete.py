import requests

product_id = input("what is the product_id you want to use?\n")

try:
    product_id = int(product_id)
except:
    product_id = None
    print(f'{product_id} not a valid id')

if product_id:
    endopoint = f"http://localhost:8000/api/products/{product_id}/delete/"
    get_response = requests.delete(endopoint)
    print(f"status: {get_response.status_code}")
    print(f'Instance was deleted? {get_response.status_code==204}')
 