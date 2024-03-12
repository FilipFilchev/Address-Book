import googlemaps

API_KEY = 'example'
map_client = googlemaps.Client(API_KEY)

address = 'Ohridsko Ezero 52, Sofia'

response = map_client.geocode(address)
print(response)