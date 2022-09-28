import xml.etree.ElementTree as ET
import requests

NIC_ZONE_URL = 'https://api.nic.ru/dns-master/zones'
headers = {"Authorization": "Bearer AnIVUfonA2mpHLWauKdlgEIHQX7izwFiQ4e2S7cyLOxnSxR8gIDrp6ydtd0MCczY6nuWbYA84xW_ZtJZtBoxTvpYB9m"}

response = requests.get(NIC_ZONE_URL, headers=headers)
response.raise_for_status()
root_node = ET.fromstring(response.text)
for child in root_node.findall('./data/zone'):
    print(child.attrib['idn-name'])
