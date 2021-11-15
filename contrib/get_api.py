import requests


url_1 = 'https://rest-demas.saude.gov.br/api/estabelecimento'
url_2 = 'https://gatewayapi.prodam.sp.gov.br:443/saude/ubs/v1.0'

my_headers = {'Authorization' : 'Bearer a5a01385ae137a7845d7df1aa663527f'}
response = requests.get(
    url_2,
    headers=my_headers
)

print(response.text)