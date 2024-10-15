# src/call_api.py

import requests
from typing import Optional, List, Dict
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_bike_station_data(contract_name: str, api_key: str) -> Optional[List[Dict]]:
    """
    Récupère les données des stations de vélos depuis l'API JCDecaux.

    Args:
        contract_name (str): Nom du contrat (e.g., 'nancy').
        api_key (str): Clé API pour l'authentification.

    Returns:
        Optional[List[Dict]]: Liste des données des stations ou None en cas d'erreur.
    """
    url = f'https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={api_key}'
    
    try:
        logger.info(f"Envoi de la requête à l'URL: {url}")
        response = requests.get(url, timeout=10)
        logger.info(f"Statut de la réponse: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        logger.info(f"Réception de {len(data)} stations.")
        return data
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Erreur HTTP: {http_err} - Statut: {response.status_code}")
    except requests.exceptions.ConnectionError:
        logger.error("Erreur de connexion: Impossible de se connecter au serveur JCDecaux.")
    except requests.exceptions.Timeout:
        logger.error("Erreur de délai d'attente: Le serveur n'a pas répondu à temps.")
    except requests.exceptions.RequestException as err:
        logger.error(f"Erreur inattendue: {err}")
    return None
