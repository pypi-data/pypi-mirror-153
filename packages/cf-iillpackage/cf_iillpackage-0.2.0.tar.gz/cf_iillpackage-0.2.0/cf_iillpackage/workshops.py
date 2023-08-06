import requests

def unreleased():
    """
        Realiza la petición y retorna los próximos talleres en CódigoFacilito a través de un objeto JSON.

        >>> type(unreleased()) == type(dict())
        True
    """
    response = requests.get('https://codigofacilito.com/api/v2/workshops/unreleased') # Consumir un API
    
    if response.status_code == 200:
        payload = response.json() # Convertir lo retornado en un diccionario
        return payload['data'] # En 'data' existe el listado de workshops
