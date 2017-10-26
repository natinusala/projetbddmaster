# projetbddmaster
Projet de BDD Evoluées de M1 Informatique

# Utilisation
Créez un fichier oauth_token.txt et mettez dedans votre token OAUTH GitHub
Le script create_sql.py permet de créer un .sql remplissant la base de données avec les données du dépôt passé en entrée
`./create_sql.py owner repo`

Donc pour le dépôt libretro/RetroArch, la commande à lancer est `./create_sql.py libretro RetroArch`

# Dépendances
 - Python 3
 - modules pip3
   - `python-dateutil`
   - `pytz`
