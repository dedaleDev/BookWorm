# BookWorm

## Dépendances : 
    - Python 3.11.8 ou ultérieur
    - De préférence un système basé sur Debian, non testé sur windows.
    - cherrypy (pip install cherrypy)
    - Apache 2 (apt install apache2) ou Nginx 
    - MariaDB (apt install mariadb-server)

## Premier lancement :  
    - Assurez vous que MariaDB et Apache2 sont bien lancés (systemctl start apache2, systemctl start mariadb)
    - Modifiez la configuration présente dans le fichiers main.py pour correspondre avec vos réglages locaux (ip, port, mot de passe de la base de donnée / site web). Des commentaires sont présents afin de faciliter la configuration.
    - Executez le fichier main.py (python3 main.py)
    - Vous serez ensuite guidé lors de l'installation de BookWorm
    - Accédez au site web via l'url saisie dans la configuration (main.py) + le numéro de port  (par défaut localhost:8080).  
    - Une fois le site lancé, vous pouvez utilisez l'un des différents utilisateurs disponibles par défaut ou vous en créer un compte.

    Compte Admin : 
            email : admin@admin.com 
            mdp : admin
    Compte HarryPotter : 
            email : harrypotter@magic.com
            mdp : harrypotter
    D'autres comptes par défaut sont disponibles, pour cela veuillez vous référer à la section utilisateur dans l'espace d'administration.

## Etat de l'application : 
    - L'état de l'application et tel que stipulé par le chahier des charges, un utilisateur non connecté peut consulter la base à tout moment.
    - Des filtres et algorythmes de tri sont disponibles pour faciliter la navigation.
    - Par contre, il a besoin de se connecter pour emprunter un livre ou le noter. 
    - L'utilisateur peux voir ses emprunts depuis son espace de compte personel. Néanmmoins,  lorsqu'il souhaite remettre un livre, une intervention de l'adminstrateur est nécessaire (comme dans une vraie bibliothèque en quelque sorte).
    - L'adminstrateur(s) peux ajouter/modifier des livres gérer les emprunts et les divers éléments présent dans la base de donnée via l'espace d'administration.
    - Toutes les fonctions qui définissent un CRUD sont présente dans une interface ergonomique et facilement utilisable.

## Les fonctionnalités prévues non réalisées (ou non prévues mais réalisées) : 
    L'ensemble des fonctions tels que stipulé dans le cahier des charges ont été implémentés exepté un filtre par format
    qui n'aurait pas été pertinent au vue de la base de donnée que j'ai constitué. En contreparti, j'ai implémenté un petit algo de tri par pertinence basé sur un système de points. Permettant ainsi des résultats bien plus efficaces.
    Ainsi si l'utilisateur saisi : "Harry Potter 7", il tombera directement sur Harry Potter tome 7 ce qui n'était pas le cas dans la version précédente de BookWorm. Car le tri était alors par ordre alphabétique.
    Un compteur du nombre de résultats à par ailleurs été ajouté par rapport à la version CLI.

## Description contenue de l'archive : 
    La partie client de BookWorm

## Pannes : 
    - En raisons d'un bugs inexepliqué de pymysql (packet sequence error) causant la deconnexion du curseur de manière aléatoire, j'ai implémenté une fonction de "retry" 
    qui est chargé de relancer automatiquement le service dans les meilleurs délais. Néanmois, dans de rare cas, il n'est pas possible de relancer le service.
    Si cela se produit une erreur packet error sequence apparaitra en rouge dans le terminal. Si cela se produit tentez simplement de recharger la page. Si celle ci refuse de se charger,  Il est alors necessaire de relancer complétement BookWorm.
