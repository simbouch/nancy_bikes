
# 🚴‍♂️ Rééquilibrage des Stations de Vélos à Nancy 🚴‍♀️

## Introduction

L'application **Rééquilibrage des Stations de Vélos à Nancy** est un outil Streamlit pour visualiser et optimiser le rééquilibrage des stations de vélos en libre-service à Nancy, France. Elle permet aux utilisateurs de choisir d'ajouter ou de collecter des vélos à des stations en fonction des besoins.

## Fonctionnalités

- **Affichage de la Carte** avec toutes les stations de vélos à Nancy.
- **Saisie de la Position du Conducteur** et calcul du meilleur itinéraire.
- **Action de Collecte ou Dépôt** de vélos selon les besoins de rééquilibrage.

## Structure du Projet

```
nancy_bikes/
├── main.py
├── src/
│   ├── route_optimizer.py
│   ├── load_bike_station.py
│   ├── map_utils.py
└── requirements.txt
```

## Installation

1. **Cloner le dépôt** :
    
    git clone https://github.com/yourusername/nancy_bikes.git
    cd nancy_bikes
    ```

2. **Installer les dépendances** :
 
    pip install -r requirements.txt
    ```

3. **Exécuter l'application** :
 
    streamlit run main.py
    ```

## Utilisation

1. Choisissez votre position de départ.
2. Sélectionnez l'action de **Collecte** ou **Dépôt** de vélos.
3. L'application vous proposera l'itinéraire optimal pour rééquilibrer les vélos.

## Licence

Ce projet est sous licence MIT.
