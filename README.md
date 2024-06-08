BOOKWORM
================

Bookworm is a personal library manager.

![192_168_1_20_8080 · 8 07am · 05-20](https://github.com/dedaleDev/BookWorm/assets/101816097/ef419c1d-f85d-4d3d-a6b3-9d9c54665615)



## Dependencies
-------------

* Python 3.11.8 or later
* Debian-based system (not tested on Windows)
* Cherrypy (`pip install cherrypy`)
* PyMySQL (`pip install pymysql`)
* Apache 2 (`apt install apache2`) or Nginx
* MariaDB (`apt install mariadb-server`)

## First launch
--------------

### Steps to follow

1. Make sure that MariaDB and Apache2 are running:
```
systemctl start apache2
systemctl start mariadb
```
2. Modify the configuration in the `main.py` file to match your local settings (ip, port, database/website password). Comments are provided to make configuration easier.
3. Run the `main.py` file:
```
python3 main.py
```
4. You will then be guided through the installation of BookWorm.
5. Access the website using the URL entered in the configuration (`main.py`) + the port number (default `localhost:8080`).


### Default accounts
---------------------

* Admin account :
	+ Email: `admin@admin.com`
	+ Password: `admin
* Harry Potter account:
	+ Email: `harrypotter@magic.com`
	+ Password: `harrypotter` * Other default accounts are available.
* Other default accounts are available, please refer to the user section in the administration area.

Welcome to BookWorm!
