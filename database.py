import pymysql

class db():
    def __init__(self) -> None:
        try :
            db =pymysql.connect(host="192.168.1.20", charset="utf8",user="root", passwd="1234",db="BookWorm")
        except Exception as e:
            print(f"Erreur : Impossible de se connecter à la base de donnée : {e}")