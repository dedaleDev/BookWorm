# BookWorm

## Dépendances : 
    - Python 3.11.8 ou ultérieur
    - cherrypy (pip install cherrypy)
    - Apache 2 (apt install apache2) ou Nginx 
    - MariaDB (apt install mariadb-server)

## Premier lancement : 
    - Assurez vous que MariaDB et Apache2 sont bien lancés (systemctl start apache2, systemctl start mariadb)
    - Executez le fichier main.py (python3 main.py)
    - Vous serez ensuite guidé lors de l'installation de BookWorm

## Etat de l'application : 
    L'ensemble des fonctions tels que stipulé dans le cahier des charges ont été implémentés.

## Pannes : 
    - En raisons d'un bugs inexepliqué de pymysql causant la deconnexion du curseur, j'ai implémenté une fonction de "retry" 
    qui est chargé de relancer automatiquement le service dans les meilleurs délais. Néanmois, dans de rare cas, il n'est pas possible de relancer le service.
    Si cela se produit une erreur packet error sequence apparaitra en rouge dans le terminal. Il est alors necessaire de relancer complétement BookWorm.
