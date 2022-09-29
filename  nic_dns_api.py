import xml.etree.ElementTree as ET
from collections import defaultdict
import requests

NIC_SERVICE = '3DNS_HOST'
NIC_ZONE = 'shockland.ru'
NIC_TOKEN = 'AXYlA9SWtJmqv0khFKu8Hi0UMMeXfK4iWbzfseBuJQirrcN6X8lhJGewWEJZ0cz6QHm2ar25Sbfsn1uE-JRrsNPr6wB'
NIC_RECORDS_URL = f'https://api.nic.ru/dns-master/services/{NIC_SERVICE}/zones/{NIC_ZONE}/records'
NIC_COMMIT_ZONE_URL = 'https://api.nic.ru/dns-master/services/3DNS_HOST/zones/shockland.ru/commit'

headers = {"Authorization": f"Bearer {NIC_TOKEN}"}


def delete_acme(id):
    response = requests.delete(f'NIC_ZONE_URL/{id}', headers=headers)
    response.raise_for_status()
    response = requests.post(NIC_COMMIT_ZONE_URL, headers=headers)
    response.raise_for_status()


def etree_to_dict(t):
    records = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        records = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        records[t.tag].update(('@' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                records[t.tag]['#text'] = text
        else:
            records[t.tag] = text
    return records

def get_acme_rr():
    response = requests.get(NIC_RECORDS_URL, headers=headers)
    response.raise_for_status()
    root_node = ET.fromstring(response.text)
    acme_records = []
    zone_records = etree_to_dict(root_node)
    for record in zone_records['response']['data']['zone']['rr']:
        if record.get('name') == '_acme-challenge':
            acme_records.append(
                                    {
                                     'acme_text': record['txt']['string'],
                                     'record_id': record['@id']
                                    }
            )
    return acme_records

if __name__ == "__main__":
    print(get_acme_rr())
