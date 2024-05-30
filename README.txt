# BookWorm

# Dépendances : 
    - Python 3.11.8 ou ultérieur
    - De préférence un système basé sur Debian, non testé sur Windows.
    - cherrypy (pip install cherrypy)
    - Apache 2 (apt install apache2) ou Nginx 
    - MariaDB (apt install mariadb-server)

# Premier lancement :  
    - Assurez-vous que MariaDB et Apache2 sont bien lancés (systemctl start apache2, systemctl start mariadb)
    - Modifiez la configuration présente dans le fichier main.py pour correspondre avec vos réglages locaux (ip, port, mot de 	passe de la base de donnée / site web). Des commentaires sont présents afin de faciliter la configuration.
    - Exécutez le fichier main.py (python3 main.py)
    - Vous serez ensuite guidé lors de l'installation de BookWorm
    - Accédez au site web via l'URL saisie dans la configuration (main.py) + le numéro de port  (par défaut localhost:8080).  
    - Une fois le site lancé, vous pouvez utiliser l'un des différents utilisateurs disponibles par défaut ou vous en créer un compte.

    Compte Admin : 
            email : admin@admin.com 
            mdp : admin
    Compte HarryPotter : 
            email : harrypotter@magic.com
            mdp : harrypotter
    D'autres comptes par défaut sont disponibles, pour cela, veuillez vous référer à la section utilisateur dans l'espace d'administration.

# État de l'application : 
    - L'état de l'application est tel que stipulé par le cahier des charges, un utilisateur non connecté peut consulter la base à tout moment.
    - Des filtres et des algorithmes de tri sont disponibles pour faciliter la navigation.
    - Par contre, l'utilisateur a besoin de se connecter pour emprunter un livre ou le noter. 
    - L'utilisateur peut voir ses emprunts depuis son espace de compte personnel. Néanmoins,  lorsqu'il souhaite remettre un livre, une intervention de l'administrateur est nécessaire (comme dans une vraie bibliothèque en quelque sorte).
    - L'administrateur(s) peut ajouter/modifier des livres, gérer les emprunts et les divers éléments présents dans la base de donnée via l'espace d'administration.
    - Toutes les fonctions qui définissent un CRUD sont présentes dans une interface ergonomique et facilement utilisable.

# Les fonctionnalités prévues non réalisées (ou non prévues, mais réalisées) : 
    L'ensemble des fonctions telles que stipulées dans le cahier des charges ont été implémentées, excepté un filtre par format et date qui n'aurait pas été pertinent au vu de la base de données que j'ai constituée. En contrepartie, j'ai implémenté un petit algorithme de tri par pertinence basé sur un système de points. Permettant ainsi des résultats bien plus efficaces.
    Ainsi si l'utilisateur saisi : "Harry Potter 7", il tombera directement sur Harry Potter tome 7 ce qui n'était pas le cas dans la version précédente de BookWorm. Le tri étant à l'époque par ordre alphabétique.
    Un compteur du nombre de résultats a par ailleurs été ajouté par rapport à la version CLI.

# Modification de la base depuis l'étape 2 :
    La base fournie dans l'étape 2 est exactement la même que celle actuelle. Seuls quelques changements mineurs ont été effectués, notamment au niveau des données de la base. La structure en elle-même n'a pas été changée.
    La nouvelle version web a nécessité de coder et de recoder de nombreux scripts de gestion de la base, notamment pour s'adapter à la gestion de mon site via API.
    J'ai du notamment effectuer d'important changement au niveau de ma fonction mkRequest() responsable de la gestion l'execution des requetes. En effet, l'utilisation d'une API a très rapidement satturé les capacités de traitement de ma base de donnée.
    Ma base de donnée recevait plusieurs requetes à la fois et n'étant pas capable de les gérer correctement elle se déconnectait causant un crash général. Afin de pallier ce problème, j'ai du faire appel à un Lock du module threading. 
    L'utilisation d'un Lock permet de s'assurer que l'ensemble des requetes sont executés dans l'ordre. 

# Description du contenu de l'archive : 
    Le répertoire data contient l'ensemble des données utilisées pour importer le jeu de données, que ce soit les fichiers CSV, les images de couverture des livres.
    La partie client de BookWorm est stockée entièrement dans le dossier www. On y retrouve cinq dossiers qui constituent l'ensemble des ressources accessibles par le web via cherrypy.
    Notamment :  
        - Dossier css  : regroupant tous les fichiers CSS. Généralement, ceux-ci sont nommés du même nom que le fichier HTML correspondant.
        - Dossier "frameworks" contient les frameworks utilisés par le site web : Bootstrap et Popper.js
        - Dossier html : les différentes pages du site.
        - Dossier img : les images du site, mais aussi celles des livres.
            - bestLivres : contient les images affichées sur la page d'accueil. Elles sont changées régulièrement par le site afin de mettre en valeur le contenu du site.
            - livres : les images des livres nommées par ISBN.
            - stars : les images utilisées pour les notes.
        - Dossier js : l'ensemble  des scripts clients permettant les requêtes API, la gestion des interactions utilisateurs et de manière générale  d'un site dynamique.
    Le répertoire de BookWorm contient par ailleurs les divers scripts Python suivants : 
        - database.py : classe python permettant la gestion complète de la base de donnée avec pymysql. Elle est responsable de la création et de l'exécution des requêtes.
        - main.py : le fichier responsable du lancement du programme. 
        - operationOnDataBase.py : fichier effectuant différentes opérations sur la base de donnée, mais n'étant pas directement lié au serveur cherrypy. Dans la version CLI de BookWorm ce fichier avait un intérêt très important puisqu'il était responsable de toutes les actions effectuées sur la base de donnée, mais son rôle a été remplacé dans ce second livrable par server.py.
        - searchEngine.py : ce fichier regroupe les différentes fonctions chargées d'effectuer les recherches dans la base de donnée. Et notamment le nouvel algorithme de tri par pertinence.
        - server.py : il s'agit du point central du site web BookWorm, il regroupe tous les points d'entrée API et la gestion de cherrypy. C'est lui qui est responsable d'utiliser la classe db (database.py) pour effectuer les différentes opérations.
        - utils.py : regroupe diverses fonctions principalement liées au formatage JSON des données avant qu'elles soient transmises par l'API de server.py.
    On trouve enfin deux fichiers .sql : 
        - backup.sql : permet de restaurer l'entièreté de la base de donnée s'il n'était pas possible de la récupérer autrement via l'exécution du code main.py.
        - template.sql : permet de créer la base de donnée ainsi que ses différentes tables (contrairement à backup.sql, ce fichier ne contient pas les données d'exemples)