import requests

def unreleased():
  # Este pedazo de String de ve al realizar el comando:
  # help(unreleased.__doc__)

  # La utilizamos para realizar pruebas simples
  """Retorna los próximos talleres en CodigoFcilito.
  >>> type(unreleased()) == type(dict())
  True
  """

  response = requests.get('https://codigofacilito.com/api/v2/workshops/unreleased')
  if (response.status_code == 200):
     payload = response.json()
     return payload['data']