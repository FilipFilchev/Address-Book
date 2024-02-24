import http.client, urllib.parse

conn = http.client.HTTPConnection('api.positionstack.com')

params = urllib.parse.urlencode({
    'access_key': 'key',
    'query': 'ul. Shipka 34, 1000 Sofia, Bulgaria',
    'limit': 1,
    })

conn.request('GET', '/v1/forward?{}'.format(params))

res = conn.getresponse()
data = res.read()

print(data.decode('utf-8'))


"""  
{"data":[
    {
        "latitude":42.685984,
        "longitude":23.326714,
        "type":"locality",
        "name":"Sofia",
        "number":null,
        "postal_code":null,
        "street":null,
        "confidence":0.6,
        "region":"Sofiya",
        "region_code":"SF",
        "county":null,
        "locality":"Sofia","administrative_area":null,"neighbourhood":null,"country":"Bulgaria","country_code":"BGR","continent":"Europe","label":"Sofia, SF, Bulgaria"}]}
"""