![masscotteOpenEeyes](https://github.com/dedaleDev/BookWorm/assets/101816097/e2ae4087-861b-41b8-8d45-9ea8cc29f71d)# BookWorm
================

![192_168_1_20_8080 · 8 07am · 05-20](https://github.com/dedaleDev/BookWorm/assets/101816097/ef419c1d-f85d-4d3d-a6b3-9d9c54665615)

Bookworm est un gestionnaire de bibliothèque personnelle.

## Dépendances
-------------

* Python 3.11.8 ou ultérieur
* Système basé sur Debian (non testé sur Windows)
* Cherrypy (`pip install cherrypy`)
* PyMySQL (`pip install pymysql`)
* Apache 2 (`apt install apache2`) ou Nginx
* MariaDB (`apt install mariadb-server`)

## Premier lancement
--------------

### Étapes à suivre

1. Assurez-vous que MariaDB et Apache2 sont bien lancés :
```
systemctl start apache2
systemctl start mariadb
```
2. Modifiez la configuration présente dans le fichier `main.py` pour correspondre avec vos réglages locaux (ip, port, mot de passe de la base de données / site web). Des commentaires sont présents afin de faciliter la configuration.
3. Exécutez le fichier `main.py` :
```
python3 main.py
```
4. Vous serez ensuite guidé lors de l'installation de BookWorm.
5. Accédez au site web via l'URL saisie dans la configuration (`main.py`) + le numéro de port (par défaut `localhost:8080`).

### Comptes par défaut
---------------------

* Compte Admin :
	+ Email : `admin@admin.com`
	+ Mot de passe : `admin`
* Compte Harry Potter :
	+ Email : `harrypotter@magic.com`
	+ Mot de passe : `harrypotter`
* D'autres comptes par défaut sont disponibles, pour cela, veuillez vous référer à la section utilisateur dans l'espace d'administration.

Bienvenue sur BookWorm !
