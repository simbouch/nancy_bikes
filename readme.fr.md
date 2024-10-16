# Application de Rééquilibrage des Stations de Vélos à Nancy

## Aperçu

Ce projet est une application web basée sur Streamlit, conçue pour aider à gérer les stations de vélos à Nancy, France. Elle propose une visualisation en temps réel des stations de vélos, en mettant en avant celles qui sont surchargées ou sous-alimentées, et fournit un itinéraire optimisé pour rééquilibrer les vélos entre les stations.

<img src="https://raw.githubusercontent.com/simbouch/nancy_bikes/refs/heads/main/assets/images/screenshot.png" width="850"/>

## Fonctionnalités

- **Carte interactive** : Affiche les emplacements de toutes les stations de vélos à Nancy, ainsi que leur statut actuel (équilibrée, surchargée, sous-alimentée).
- **Localisation du conducteur** : Permet au conducteur de saisir sa position actuelle et de la visualiser sur la carte.
- **Optimisation d'itinéraire** : Calcule le meilleur itinéraire pour collecter ou déposer des vélos afin de rééquilibrer les stations.
- **Données en temps réel** : Récupère des données en temps réel depuis l'API JCDecaux pour garder la carte à jour.

## Comment ça fonctionne

1. **Chargement des données** :
   - L'application récupère des données en temps réel sur les stations de vélos à Nancy depuis l'API JCDecaux, à l'aide de la fonction `get_bike_station_data` dans `call_api.py`. Ces données incluent le nombre de vélos disponibles, les places libres et les coordonnées des stations.
   - Les données sont traitées dans `load_bike_station.py` et renvoyées sous forme de DataFrame Pandas.

2. **Classification des stations de vélos** :
   - Les stations sont classées comme **surchargées** (trop de vélos), **sous-alimentées** (pas assez de vélos), ou **équilibrées**. Cela est effectué dans `balance_analysis.py` en utilisant les données de vélos disponibles et la capacité des stations.

3. **Création de la carte** :
   - Une carte centrée sur Nancy est créée à l'aide de Folium dans `map_utils.py`.
   - Les stations de vélos sont ajoutées à la carte avec des marqueurs colorés selon leur classification : rouge pour surchargée, vert pour sous-alimentée, et bleu pour équilibrée.

4. **Localisation du conducteur** :
   - L'utilisateur saisit sa position actuelle, soit manuellement en entrant la latitude et la longitude, soit en utilisant la position par défaut (Nancy, France). La position du conducteur est ensuite affichée sur la carte.

5. **Optimisation d'itinéraire** :
   - L'application utilise OSMnx pour créer un réseau routier de Nancy (`create_nancy_graph` dans `route_optimizer.py`).
   - En fonction de la position du conducteur et des données des stations, l'application calcule la meilleure station pour collecter ou déposer des vélos afin de rééquilibrer le système. Cela est fait à l'aide de la fonction `find_best_station`, qui trouve le chemin le plus court vers la station optimale en utilisant NetworkX.

6. **Affichage et interaction** :
   - L'itinéraire calculé est affiché sur la carte, avec une infobulle fournissant des détails tels que la distance jusqu'à la station et le nombre de vélos à collecter ou à déposer.
   - Les utilisateurs peuvent mettre à jour leur localisation, les paramètres du véhicule et rafraîchir les données en temps réel, garantissant des informations toujours à jour.

## Structure du projet

```
.
├── src
│   ├── __init__.py
│   ├── balance_analysis.py
│   ├── call_api.py
│   ├── load_bike_station.py
│   ├── map_utils.py
│   └── route_optimizer.py
├── main.py
├── requirements.txt
```

### Description des dossiers et fichiers

- **src** : Contient tous les scripts utilitaires pour le chargement des données, l'analyse et la création de la carte.
  - `balance_analysis.py` : Classe les stations de vélos en fonction de leur équilibre actuel (surchargée, sous-alimentée, ou équilibrée).
  - `call_api.py` : Récupère des données en temps réel à partir de l'API JCDecaux.
  - `load_bike_station.py` : Gère le chargement et le prétraitement des données des stations de vélos.
  - `map_utils.py` : Contient des fonctions pour créer la carte, ajouter des stations et des positions de conducteur, et afficher des itinéraires optimisés.
  - `route_optimizer.py` : Optimise l'itinéraire pour rééquilibrer les vélos entre les stations.
- **main.py** : Le script principal de l'application, construit avec Streamlit. Il fournit l'interface utilisateur pour interagir avec l'application, charger des données, afficher des cartes et calculer des itinéraires.
- **requirements.txt** : Liste des dépendances requises pour exécuter le projet.

## Système de notation

Le système de notation dans l'**Application de Rééquilibrage des Vélos à Nancy** est crucial pour déterminer la meilleure station pour **collecter** ou **déposer** des vélos. Il permet de rééquilibrer les stations en prenant en compte la charge actuelle de chaque station et la position de l'utilisateur.

### Facteurs clés

Le système de notation équilibre deux facteurs principaux :

1. **Distance** : La proximité d'une station par rapport à la position actuelle de l'utilisateur.
2. **Disponibilité** : Le nombre de vélos disponibles à la station (pour la collecte) ou le nombre de places libres (pour le dépôt).

### Formule de notation

La formule équilibre la **disponibilité** et la **distance** pour attribuer un score à chaque station. Le score permet de prioriser les stations, les scores les plus élevés indiquant les stations les mieux adaptées pour le rééquilibrage.

#### Pour la collecte de vélos :
- **Formule** :

   <img src="https://raw.githubusercontent.com/simbouch/nancy_bikes/refs/heads/main/assets/images/formula_collecting.png"/>

- **Explication** :
  - Le **numérateur** (`available_bikes`) représente le nombre de vélos disponibles à la station. Plus il y a de vélos, plus le score est élevé.
  - Le **dénominateur** (`distance + 1`) pénalise les stations plus éloignées de l'utilisateur, tandis que le `+1` empêche une division par zéro.

#### Pour le dépôt de vélos :
- **Formule** :

   <img src="https://raw.githubusercontent.com/simbouch/nancy_bikes/refs/heads/main/assets/images/formula_depositing.png"/>

- **Explication** :
  - Le **numérateur** (`available_bike_stands`) représente le nombre de places libres à la station. Plus il y a de places disponibles, plus le score est élevé.
  - Le **dénominateur** (`distance + 1`) fonctionne de manière similaire à la formule de collecte, en priorisant les stations les plus proches tout en évitant une division par zéro.

### Pourquoi ajouter `+1` à la distance ?

Le `+1` garantit que :
- **Division par zéro** : Lorsque l'utilisateur est à la station (distance = 0), la formule ne divise pas par zéro.
- **Équilibre des poids** : Cela empêche la distance d'avoir une influence trop forte, permettant à la disponibilité de jouer un rôle plus important dans la décision.

### Critères de décision

- **Pour la collecte** : Les stations avec plus de vélos disponibles sont priorisées, garantissant que celles qui ont un surplus de vélos sont rééquilibrées en premier.
- **Pour le dépôt** : Les stations avec plus de places disponibles sont priorisées, garantissant que les stations sous-alimentées reçoivent des vélos.

### Avantages du système de notation

- **Efficacité** : Le système garantit que l'utilisateur est dirigé vers la meilleure station, économisant du temps et des efforts tout en maintenant l'équilibre des stations.
- **Dynamique** : Le système de notation s'ajuste en temps réel lorsque l'utilisateur se déplace ou que l'état des stations change, garantissant des décisions optimales tout au long du processus.

## Déploiement sur Streamlit Cloud

L'application est déployée sur Streamlit Cloud et peut être consultée via (https://nancy-bikes.streamlit.app/).

### Gestion des Secrets Streamlit

Pour garder la clé API sécurisée, le projet utilise le système de gestion des secrets intégré à Streamlit. Le fichier `secrets.toml` contient la clé API et n'est pas partagé publiquement pour des raisons de sécurité.

Exemple de `secrets.toml` :
```toml
[secrets]
JCDECAUX_API_KEY = "votre_cle_api_jcdecaux_ici"
```
Assurez-vous de stocker ce fichier dans le répertoire `.streamlit/` et de l'exclure du contrôle de version à l'aide de `.gitignore`.

## Comment exécuter

1. **Cloner le dépôt** :
    ```bash
    git clone <votre-url-depot>
    cd <dossier-du-projet>
    ```

2. **Installer les dépendances** :
    Assurez-vous

 que Python est installé, puis exécutez :
    ```bash
    pip install -r requirements.txt
    ```

3. **Exécuter l'application** :
    ```bash
    streamlit run main.py
    ```

4. **Interagir avec l'application** :
    - Choisissez si vous souhaitez collecter ou déposer des vélos.
    - Visualisez l'itinéraire optimisé sur la carte.

## Intégration de l'API

L'application récupère des données en temps réel depuis l'API JCDecaux en utilisant le contrat `nancy`. Assurez-vous d'ajouter votre propre clé API dans le fichier `load_bike_station.py` pour que la récupération des données fonctionne correctement.

## Exigences

- Python 3.x
- Streamlit
- Pandas
- Geopy
- Folium
- OSMnx
- NetworkX

Pour une liste complète des dépendances, consultez le fichier `requirements.txt`.

## Licence

Ce projet est open-source et libre d'utilisation.