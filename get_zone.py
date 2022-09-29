import xml.etree.ElementTree as ET
import requests

NIC_ZONE_URL = 'https://api.nic.ru/dns-master/zones'
headers = {"Authorization": "Bearer AxEStRu6tNjee3z7hkjgf7sSpT--5OriyJbPEzKwcaYWBNK_hll8ywGy8z-QAczC2xySn-_GUV30QK3RZRr9XvOQrdK"}

response = requests.get(NIC_ZONE_URL, headers=headers)
response.raise_for_status()
root_node = ET.fromstring(response.text)
for child in root_node.findall('./data/zone'):
    print(child.attrib['idn-name'])
