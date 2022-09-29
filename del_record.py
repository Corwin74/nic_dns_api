import requests

NIC_TOKEN = 'AbYIy4StV_-2GNch4L4RvOp_-5tUpDvipeOqO01-I7XuR-HRDbMLIlZoF8FeTcz-bQvIgf2oI3gwjCffmT7__FrQunN'
NIC_ZONE_URL = 'https://api.nic.ru/dns-master/services/3DNS_HOST/zones/shockland.ru/records'
NIC_COMMIT_ZONE_URL = 'https://api.nic.ru/dns-master/services/3DNS_HOST/zones/shockland.ru/commit'

headers = {"Authorization": f"Bearer {NIC_TOKEN}"}

response = requests.delete(NIC_ZONE_URL+'/51580744', headers=headers)
response.raise_for_status()
response = requests.post(NIC_COMMIT_ZONE_URL, headers=headers)
response.raise_for_status()
print('Deleted')
