from django.db import connection

def list_event():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dbo.Evenement;")
        liste = cursor.fetchall()

    return liste

def add_event(nom_event):
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Evenement (nom_evenement) VALUES (%s);", [nom_event])
        return True
    except Exception as e:
        print("Erreur lors de l'insertion de l Evenement :", e)
        return False
    
def un_event(id_investisseur):
    with connection.cursor() as cursor:
        cursor.execute(""" 
                       SELECT * FROM dbo.Evenement
                       WHERE id IN ( SELECT id_evenement FROM dbo.Investisseur WHERE id = %s ); """, [id_investisseur])
        liste = cursor.fetchone()
    
    return liste
