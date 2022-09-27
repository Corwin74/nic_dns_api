import requests
from requests.auth import HTTPBasicAuth


CLIENT_NAME = 'd8b0a9a30bfd952bc5f6452b918b740d'
USER_NAME =  '2611203/NIC-D'.encode('utf-8')
CLIENT_PASSWORD = 'aMY_rNjuuJUnd7rqE1b6GxD8cfoK2XpUA5GHzsKZKtw'
USER_PASSWORD = 'ycbzrXE6RVpCTcf'.encode('utf-8')
NIC_DNS_OAUTH2_URL = 'https://api.nic.ru/oauth/token'



headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
request_body =  {
                "grant_type": "password",
                "username": USER_NAME,
                "password": USER_PASSWORD,
                "scope": "fick",
}


response = requests.post(
                  NIC_DNS_OAUTH2_URL,
                  auth=HTTPBasicAuth(CLIENT_NAME, CLIENT_PASSWORD),
                  data=request_body,
                  headers=headers,
)
response.raise_for_status()
print(response.text)
