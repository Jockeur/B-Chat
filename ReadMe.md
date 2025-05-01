# B-Chat

Ce projet est un projet réalisé en classe de NSI.
Notre but derrière ce projet était de nous amuser en comprenant comment fonctionne une messagerie en ligne.

## Table of Contents

- [Pré-requis](#pré-requis)
- [Démarrage](#démarrage)
- [Arrêt](#arrêt)
- [Utilisation](#utilisation)

## Pré-requis
Afin de pouvoir démarrer le projet vous devez avoir installer :
- Python 3.13
- Pygame

Pour installer :
- Python 3.13 : https://www.python.org/downloads/
- Pygame : ```pip install pygame``` Ou ```python -m pip install pygame```

## Démarrage

### Lancer le serveur
#### Windows
1. Se rendre dans le dossier "serveur"
2. Lancer le fichier "server.bat"

#### Linux
1. Se rendre dans le dossier "serveur"
2. Lancer le fichier "server.sh"


### Lancer l'application
#### Windows
1. Se rendre dans le dossier "client"
2. Lancer le fichier "bchat.bat"

#### Linux
1. Se rendre dans le dossier "client"
2. Lancer le fichier "bchat.sh"

## Arrêt
Une fois que vous aurez fini avec l'application vous voudrez certainement l'arrêter. De même pour le serveur.

### Application
Afin d'arrêter l'application il vous suffit d'appuyer sur la croix en haut à droite ou d'utiliser la combinaison Alt + F4 comme toute application.

Pour arrêter le serveur, il vous suffira de fermer le terminal dans lequel ce dernier s'éxécute.


## Utilisation

Une fois l'application lancée, une interface apparait vous demandant d'entrer un pseudonyme.
Les seuls utilisateurs disponible sont
- Pseudo: John
  Mot de passe: test

- Pseudo: Jane
  Mot de passe: test

Une fois connecté, l'interface principale s'affiche.
Il y a à gauche une liste de contact avec une barre de recherche. Vous pouvez cliquer sur l'un d'entre eux afin d'afficher la discussion avec ce dernier

Une fois un contact sélectionné, à droite s'affichera la discussion avec ce dernier. Vous pouvez utiliser la barre bleue afin d'écrire un message et l'envoyer. Vous pouvez aussi utiliser la molette de la souris afin de faire défiler les messages.