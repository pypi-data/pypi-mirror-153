import requests

def dogsList():
    """Retorna un listado de las razas de perros de la API pública.
    >>> type(dogsList()) == type(dict())
    True
    """
    response = requests.get('https://dog.ceo/api/breeds/list/all')

    if response.status_code == 200:
        payload = response.json()
        return payload['message']