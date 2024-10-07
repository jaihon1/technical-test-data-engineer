# Réponses du test

## _Utilisation de la solution (étape 1 à 3)_

1. Cloner le repository
2. Naviguer vers le root directory du projet
3. Configurer un environnement virtuel Python. Python 3.10.13 a été utilisé pendant le développement de la version v1.0.0 de cette solution. L'environnement virtuel a été configuré avec la commande suivante:
   - `python -m venv ./venv` et activé avec `source venv/bin/activate`
4. Installer toutes les dépendances. `pip install -r requirements.txt`
5. Lancer le serveur Moovitamix_FastAPI. Dans un autre processus terminal (avec l'environnement virtuel activé), naviguer vers src/moovitamix_fastapi et exécuter `python -m uvicorn main:app`
6. Dans le root directory du projet, utiliser le script suivant pour exécuter la solution de flux de données: `sh scripts/run_ingest.sh` (ou bash scripts/run_ingest.sh selon la configuration de votre machine)
7. Une fois le script terminé, la solution aura complété les tâches suivantes :
   - Récupère les données depuis l'endpoint cible qui a été fourni dans le script run_ingest.sh
   - Valide les données selon la version v1.0.0 de l'ApiSchema. Veuillez noter que la première version de cette solution ne nécessite que les ID (id des utilisateurs, id des pistes et user_id de Listen_History) comme champs obligatoires. La base est configurée pour faciliter et intégrer facilement de nouvelles spécifications de validation dans les itérations futures.
   - Mappe et prépare les données validées dans un format DataSchema v1.0.0 prêt à être sauvegardé.
8. Pour executer les tests. Naviguer vers le root directory du projet: `python -m pytest`

### Notes concernant la solution
1. Le principal bottleneck de cette solution est la récupération des données depuis l'API via des requêtes réseau. Par conséquent, cette solution v1.0.0 utilise des requêtes API asynchronous par batch pour récupérer les données.
2. Certaines statistiques recueillies lors du développement montrent qu'il faut ~9,90 secondes pour 1 000 requêtes en utilisant le traitement asynchronous par batch, contre ~13,72 secondes pour 1 000 requêtes en utilisant le traitement asynchronous séquentiel.
2. Pour la version v1.0.0 de la solution, chaque processus déterminera le nombre total de requêtes nécessaires pour obtenir l'ensemble complet des données. D'après les tests effectués pendant le développement, il est recommandé d'effectuer un maximum de 2 000 à 2 500 requêtes simultanées au MoovitamixFastAPI.
2. Cette solution v1.0.0 est basée sur les exigences fournies par le client, avec la compréhension que ces exigences peuvent évoluer à tout moment. Comme nous n'avons pas de contrôle sur les changements potentiels côté client, nous nous efforçons de garantir que notre solution initiale repose sur une base solide, est suffisamment simple, répond à toutes les exigences et est assez flexible pour permettre des ajustements itératifs à un coût minimal.

#### Feedback on the API
1. Endpoint /users -> Renommage de l'attribut "favorite_genres" au singulier (confusion avec une liste de genres).
2. Il n'y a aucune spécification concernant l'aspect temporel de l'historique des morceaux écoutés. Avoir des timestamp pour chaque chanson jouée pourrait être potentiellement bénéfique. Pour la version v1.0.0, l'hypothèse suivante a été faite: l'historique est représenté de gauche à droite, où l'ID du Track le plus à gauche correspond au morceau le plus ancien joué.

## Questions (étapes 4 à 7)

### Étape 4
Les données sont hautement relationnelles ; par conséquent, une base de données relationnelle conviendrait bien à cette solution, car elle est simple à configurer et à utiliser. Veuillez noter que pour cette version de la solution, toutes les versions des données sont écrites dans les mêmes tables. Au fur et à mesure que la solution évoluera et que le volume de données augmentera, des modifications pourront être apportées à cette structure pour garantir que seules les dernières versions soient stockées dans ces schémas, tandis que les versions historiques seront déplacées vers des tables séparées avec optimisation et compression. Les schémas de données suivants seront utilisés pour la version 1.0.0 :

#### Users Schema
```sql
id INT NOT NULL,  -- Must be provided
version_id INT NOT NULL,  -- Must be provided
first_name VARCHAR(256) DEFAULT NULL,
last_name VARCHAR(256) DEFAULT NULL,
email VARCHAR(256) UNIQUE DEFAULT NULL,
gender VARCHAR(128) DEFAULT NULL,
favorite_genres VARCHAR(256) DEFAULT NULL,
created_at TIMESTAMP DEFAULT NULL,
updated_at TIMESTAMP DEFAULT NULL,
PRIMARY KEY (id, version_id)  -- Composite primary key on id and version_id
FOREIGN KEY (version_id) REFERENCES Versions(id)  -- Foreign key referencing Versions table
```

#### Tracks Schema
```sql
id INT NOT NULL,  -- Must be provided
version_id INT NOT NULL,  -- Must be provided
name VARCHAR(256) DEFAULT NULL,
artist VARCHAR(256) DEFAULT NULL,
songwriters VARCHAR(256) DEFAULT NULL,
duration VARCHAR(128) DEFAULT NULL,
genres VARCHAR(256) DEFAULT NULL,
album VARCHAR(256) DEFAULT NULL,
created_at TIMESTAMP DEFAULT NULL,
updated_at TIMESTAMP DEFAULT NULL,
PRIMARY KEY (id, version_id)  -- Composite primary key on id and version_id
FOREIGN KEY (version_id) REFERENCES Versions(id)  -- Foreign key referencing Versions table
```

#### ListenHistory Schema
```sql
user_id INT NOT NULL,  -- Must be provided
track_id INT NOT NULL,  -- Must be provided
version_id INT NOT NULL,  -- Must be provided
created_at TIMESTAMP DEFAULT NULL,
updated_at TIMESTAMP DEFAULT NULL,
PRIMARY KEY (user_id, track_id, version_id),  -- Composite primary key on user_id, track_id, and version_id
FOREIGN KEY (user_id) REFERENCES Users(id),  -- Foreign key referencing Users table
FOREIGN KEY (track_id) REFERENCES Tracks(id)  -- Foreign key referencing Tracks table
FOREIGN KEY (version_id) REFERENCES Versions(id)  -- Foreign key referencing Versions table
```

#### Versions Schema:
Used to track different versions of the dataset.
```sql
id INT NOT NULL,  -- Must be provided
title VARCHAR(256) DEFAULT NULL,
created_at TIMESTAMP DEFAULT NULL,
expiry_at TIMESTAMP DEFAULT NULL,
PRIMARY KEY (id)  -- Primary key on id
```

### Étape 5
Regarding the health of the pipeline, the goal was to establish a strong foundation that is simple and flexible enough to adapt to changes in future iterations. A local logging mechanism has been set up that currently logs all initiated network requests, indicating whether they were successful or failed. If a request is successful, the system also logs whether it passed validation. Additionally, after each batch request is completed, metrics regarding the throughput of the influx module are logged, including the number of requests per second and the number of processed data points per second.

This is just the foundation of the project; many more items can be logged in future iterations depending on the client's specifications.

Concernant la santé du pipeline, l'objectif était de mettre en place une base solide, simple et suffisamment flexible pour s'adapter aux changements des futures itérations. Un mécanisme de logging local a été mis en place, qui enregistre actuellement toutes les requêtes réseau initiées, en indiquant si elles ont réussi ou échoué. Si une requête est réussie, le système enregistre également si elle a passé la validation. De plus, après chaque requête par lot, des métriques relatives au débit du module d'influx sont journalisées, notamment le nombre de requêtes par seconde et le nombre de points de données traités par seconde.

Ce n'est que la base du projet, beaucoup d'autres éléments pourront être journalisés dans les futures itérations, selon les spécifications du client.

### Étape 6
La plateforme musicale du client, similaire à Spotify, a des exigences fondamentales pour la génération de recommandations. L'une de ces exigences est la capacité de demander des recommandations pour un utilisateur spécifique ou un ensemble d'utilisateurs. Ce processus doit être initié via internet et rendu disponible sur tout appareil où leur plateforme fonctionne actuellement.

Pour ce faire, un service stateless (qui peut être horizontally scalable) offrant une API à ses clients peut être mis en place. Ce service renvoie des recommandations générées par le modèle d'inférence en fonction des données input fournies. Avec cette configuration, la solution musicale sur les appareils peut être configurée pour interroger le modèle d'inférence, récupérer les résultats et les afficher à l'utilisateur.

### Étape 7
Dans le real-world, des industries comme l'industrie musicale sont dynamiques et évoluent au fil du temps. De nouveaux artistes, chansons, genres et langues sont continuellement introduits, tandis que d'autres peuvent être discrètement retirés de la circulation. Par conséquent, lors de l'utilisation du système de recommandation, il est essentiel de surveiller les performances et de s'assurer que les modèles en production respectent les standards établies.

Dans notre scénario, un des metrique de production critique est le taux de click-rate des options qui ont été recommandées. En termes simples, cet indicateur montre à quelle fréquence une recommandation a été vue, sélectionnée ou aimée par les utilisateurs. Suivre cet indicateur fournit des informations en temps réel sur le comportement et la santé du système de recommandation. Des threshold et des déclencheurs peuvent être mis en place pour collecter de nouvelles données et réentraîner les modèles en réponse à certains déclencheurs. Les tendances dans l'industrie musicale peuvent émerger rapidement, il est donc crucial que le système de recommandation soit adaptable aux nouvelles données.

Idéalement, le processus de réentraînement ressemblerait à ceci: une fois que nous savons qu'il est nécessaire d'exécuter un réentraînement du modèle, nous préparons la nouvelle version des données, réentraînons un nouveau modèle, le déployons en production, puis transférons le trafic réseau de l'ancien modèle vers le nouveau (ou seulement une partie du traffic pour débuter).

L'approche suggérée précédemment était une "online method". Cependant, il existe également diverses "offline method". Par exemple, les données peuvent être analysées périodiquement pour identifier tout changement ou modification dans les distributions statistiques des différentes features du dataset. Naturellement, si les données évoluent au fil du temps en raison de tendances et d'événements du monde réel, cela pourrait indiquer que les modèles en production pourraient également nécessiter des ajustements.
