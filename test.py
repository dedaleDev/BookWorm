
 La requête à échouée : SELECT * FROM `Livre` WHERE `ISBN` LIKE 2070624544;
---, Erreur : Packet sequence number wrong - got 1 expected 17, ligne : 121
Args :  ['2070624544']
Nombre de placeholders : 1
Nombre d'arguments : 1
--------------------------------------------------
 La requête à échouée : SELECT * FROM `Livre` WHERE `ISBN` LIKE 2070615367;
---, Erreur : Packet sequence number wrong - got 101 expected 17, ligne : 121
 La requête à échouée : SELECT * FROM `Livre` WHERE `ISBN` LIKE 2070572676;
---, Erreur : (2013, 'Lost connection to MySQL server during query'), ligne : 121
Args :  ['2070572676']
Nombre de placeholders : 1
 La requête à échouée : SELECT * FROM `Auteur` WHERE `ID` = 31;
---, Erreur : Packet sequence number wrong - got 111 expected 17, ligne : 121Args :  ['2070615367']
DATA ()
192.168.1.28 - - [18/May/2024:15:29:15] "GET /getLivre?isbn=2070624544 HTTP/1.1" 200 33 "http://192.168.1.20:8080/account" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

Args :  [31]
Nombre de placeholders : 1
Nombre d'arguments : 1
--------------------------------------------------
Une erreur est survenue lors de la recherche de l'auteur :tuple index out of range, ligne : 38
######### <class 'pymysql.cursors.Cursor'> <pymysql.cursors.Cursor object at 0x7fa5a17ad880> selectPointDeVenteByAdresse ('17, avenue Victor-Hugo Centre commercial Victor-Hugo - 26000  Valence\n\n',) SELECT Nom FROM `Point de vente` WHERE `Adresse` LIKE 17, avenue Victor-Hugo Centre commercial Victor-Hugo - 26000  Valence

;######### <class 'pymysql.cursors.Cursor'> <pymysql.cursors.Cursor object at 0x7fa5a17ad880> selectAuteurByID (2,) SELECT * FROM `Auteur` WHERE `ID` = 2;
######### <class 'pymysql.cursors.Cursor'> <pymysql.cursors.Cursor object at 0x7fa5a17ad880>
 La requête à échouée : SELECT * FROM `Auteur` WHERE `ID` = 2;
---, Erreur : (0, ''), ligne : 121Nombre de placeholders : 1
Nombre d'arguments : 1
--------------------------------------------------
DATA []
Nombre d'arguments : 1
--------------------------------------------------
DATA []

Args :  [2]
Nombre de placeholders : 1
Nombre d'arguments : 1
--------------------------------------------------
######### <class 'pymysql.cursors.Cursor'> <pymysql.cursors.Cursor object at 0x7fa5a17ad880> selectPointDeVenteByAdresse ('31 rue Madier de Montjau\n26000 Valence',) SELECT Nom FROM `Point de vente` WHERE `Adresse` LIKE 31 rue Madier de Montjau
26000 Valence;
######### <class 'pymysql.cursors.Cursor'> <pymysql.cursors.Cursor object at 0x7fa5a17ad880>
 La requête à échouée : SELECT Nom FROM `Point de vente` WHERE `Adresse` LIKE 17, avenue Victor-Hugo Centre commercial Victor-Hugo - 26000  Valence

;
---, Erreur : (0, ''), ligne : 121
Args :  ['17, avenue Victor-Hugo Centre commercial Victor-Hugo - 26000  Valence\n\n']
Nombre de placeholders : 1
Nombre d'arguments : 1
--------------------------------------------------

######### <class 'pymysql.cursors.Cursor'> <pymysql.cursors.Cursor object at 0x7fa5a17ad880> selectLivreByISBN ('1041834365',) SELECT * FROM `Livre` WHERE `ISBN` LIKE 1041834365;
######### <class 'pymysql.cursors.Cursor'> <pymysql.cursors.Cursor object at 0x7fa5a17ad880>
 La requête à échouée : SELECT Nom FROM `Point de vente` WHERE `Adresse` LIKE 31 rue Madier de Montjau
26000 Valence;
---, Erreur : (0, ''), ligne : 121
Args :  ['31 rue Madier de Montjau\n26000 Valence']
Nombre de placeholders : 1
Nombre d'arguments : 1
--------------------------------------------------
######### <class 'pymysql.cursors.Cursor'> <pymysql.cursors.Cursor object at 0x7fa5a17ad880>
 La requête à échouée : SELECT * FROM `Livre` WHERE `ISBN` LIKE 1041834365;
---, Erreur : (0, ''), ligne : 121
Args :  ['1041834365']
Nombre de placeholders : 1
Nombre d'arguments : 1
--------------------------------------------------
DATA []
192.168.1.28 - - [18/May/2024:15:29:15] "GET /getLivre?isbn=2070615367 HTTP/1.1" 200 33 "http://192.168.1.20:8080/account" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
192.168.1.28 - - [18/May/2024:15:29:15] "GET /getLivre?isbn=2070572676 HTTP/1.1" 200 33 "http://192.168.1.20:8080/account" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
192.168.1.28 - - [18/May/2024:15:29:15] "GET /getLivre?isbn=2017010090 HTTP/1.1" 200 1283 "http://192.168.1.20:8080/account" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
192.168.1.28 - - [18/May/2024:15:29:15] "GET /getLivre?isbn=2070615367 HTTP/1.1" 200 1272 "http://192.168.1.20:8080/account" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
192.168.1.28 - - [18/May/2024:15:29:15] "GET /getLivre?isbn=1041834365 HTTP/1.1" 200 33 "http://192.168.1.20:8080/account" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
