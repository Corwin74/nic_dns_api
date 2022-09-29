import xml.etree.ElementTree as ET
from collections import defaultdict
import requests

NIC_SERVICE = '3DNS_HOST'
NIC_ZONE = 'shockland.ru'
NIC_TOKEN = 'AxEStRu6tNjee3z7hkjgf7sSpT--5OriyJbPEzKwcaYWBNK_hll8ywGy8z-QAczC2xySn-_GUV30QK3RZRr9XvOQrdK'
NIC_RECORDS_URL = f'https://api.nic.ru/dns-master/services/{NIC_SERVICE}/zones/{NIC_ZONE}/records'
NIC_COMMIT_ZONE_URL = 'https://api.nic.ru/dns-master/services/3DNS_HOST/zones/shockland.ru/commit'

headers = {"Authorization": f"Bearer {NIC_TOKEN}"}


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


def add_acme_record(text):

    template = f'''
        <?xml version="1.0" encoding="UTF-8" ?>
            <request>
                <rr-list>
                    <rr>
                        <name>_acme-challenge</name>
                        <type>TXT</type>
                            <txt>
                                <string>
                                    {text}
                                </string>
                            </txt>
                    </rr>
                </rr-list>
            </request>
        '''

    response = requests.put(NIC_RECORDS_URL, headers=headers, data=template)
    response.raise_for_status()
    response = requests.post(NIC_COMMIT_ZONE_URL, headers=headers)
    response.raise_for_status()
    return response.text


def delete_acme_record(record_id):
    response = requests.delete(f'{NIC_RECORDS_URL}/{record_id}', headers=headers)
    response.raise_for_status()
    response = requests.post(NIC_COMMIT_ZONE_URL, headers=headers)
    response.raise_for_status()
    return response.text


def get_acme_records():
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
    print(delete_acme_record('52489584'))
