# projetbddmaster
Projet de BDD Evoluées de M1 Informatique

# Utilisation
Créez un fichier `oauth_token.txt` et mettez dedans votre token OAUTH GitHub

Le script `create_json.py` permet de créer un .json contenant les données brutes du dépôt donné en entrée (le traitement peut être long sur les gros dépôts comme RetroArch)

`./create_sql.py owner repo`

Le script `populate_mongodb.py` prend le .json créé par le premier script, et remplit la base de données MongoDB locale avec en utilisant `mongoimport`

Donc pour le dépôt `libretro/RetroArch`, la commande à lancer est `./create_sql.py libretro RetroArch`

# Dépendances
 - Python 3
 - modules pip3
   - `python-dateutil`
   - `pytz`
