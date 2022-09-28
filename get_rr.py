import xml.etree.ElementTree as ET
import requests

NIC_ZONE_URL = 'https://api.nic.ru/dns-master/services/3DNS_HOST/zones/shockland.ru/records'
headers = {"Authorization": "Bearer AHixhWEVHbJucu3EK46TtdjOkcoKL42ijDqda3ZGSWRgPqaDvFsE5Iet6fTyncz69m0eCk8YgxC4F77J-2DkN6nE_xk"}

response = requests.get(NIC_ZONE_URL, headers=headers)
response.raise_for_status()
root_node = ET.fromstring(response.text)
for child in root_node.findall('./data/zone/rr'):
    if txt_record := child.findall('txt'):
        print('txt')
        print(child.get('id'))
        print(child.attrib['id'])
