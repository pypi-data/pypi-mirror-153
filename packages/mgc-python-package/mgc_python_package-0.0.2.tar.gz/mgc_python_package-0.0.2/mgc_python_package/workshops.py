import requests

def unreleased():
   '''
    Return the next codigo facilito's workshops
    >>> type(unreleased()) == type(dict())
    True
   '''
   response = requests.get('https://codigofacilito.com/api/v2/workshops/unreleased')
   if response.status_code == 200:
      payload = response.json()
      return payload['data']