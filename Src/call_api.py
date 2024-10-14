import requests

# URL de l'API
contract_name = 'nancy'
api_key = '06f91bb37651caa12b9199add8c0a32d07c0a268'
url = f'https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={api_key}'

# Faire un appel GET
response = requests.get(url)

# Vérifier si l'appel a réussi
if response.status_code == 200:
    # Si succès, afficher les données
    data = response.json()  # Si l'API renvoie du JSON
    print(data)
else:
    # Sinon, afficher le code d'erreur
    print(f"Erreur {response.status_code}")
