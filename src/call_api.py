
# src/call_api.py

import requests


def get_bike_station_data(contract_name, api_key):
    # URL de l'API
    url = f'https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={api_key}'

    try:
        # Faire un appel GET
        response = requests.get(url)
        response.raise_for_status()  # Vérifier les erreurs HTTP

        # Si succès, retourner les données JSON
        data = response.json()
        try:
            liste_id_to_remove = [30, 29, 34, 33, 3, 9]
            filtered_data = [item for item in data if item['number'] not in liste_id_to_remove]
            return filtered_data
        except:
            return data

    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP: {http_err}")
    except requests.exceptions.ConnectionError:
        print("Erreur de connexion: Impossible de se connecter au serveur JCDecaux.")
    except requests.exceptions.Timeout:
        print("Erreur de délai d'attente: Le serveur n'a pas répondu à temps.")
    except requests.exceptions.RequestException as err:
        print(f"Erreur: {err}")
    return None
