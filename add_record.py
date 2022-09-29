import requests

NIC_TOKEN = 'AGxHgiPTYWRIFJOsKYgUrxgdGKGXRFeioaNXkh5duqFbWTJQCzZ8My1tPg7pGczadtrxYVWurpZlz4twm7tZ0GkSW4G'
NIC_ZONE_URL = 'https://api.nic.ru/dns-master/services/3DNS_HOST/zones/shockland.ru/records'
NIC_COMMIT_ZONE_URL = 'https://api.nic.ru/dns-master/services/3DNS_HOST/zones/shockland.ru/commit'

ACME = 'Putin'
zz = f'''
<?xml version="1.0" encoding="UTF-8" ?>
    <request>
        <rr-list>
            <rr>
                <name>_acme-challenge</name>
                <type>TXT</type>
                    <txt>
                        <string>
                            {ACME}
                        </string>
                    </txt>
            </rr>
        </rr-list>
    </request>
'''


headers = {"Authorization": f"Bearer {NIC_TOKEN}"}

response = requests.put(NIC_ZONE_URL, headers=headers, data=zz)
response.raise_for_status()
response = requests.post(NIC_COMMIT_ZONE_URL, headers=headers)
response.raise_for_status()
print('Added')
