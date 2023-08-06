import requests

def lastArticles():
    """Retorna los ultimos 20 articulos publicados en CódigoFacilito.
    
    >>> type(lastArticles()) == type(list())
    True
    """

    response = requests.get('https://codigofacilito.com/api/v2/articles')

    if response.status_code == 200:
        payload = response.json()
        return payload['data']["articles"]
