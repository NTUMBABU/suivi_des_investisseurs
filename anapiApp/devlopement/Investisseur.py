
from django.db import connection
from django.db import transaction

class Investisseur:
    def __init__(self, id='', identite_investisseur="", personnalite_juridique="", nom_entreprise="", qualification="", adresse_email="", telephone="", pays="", adresse_entreprise="", boite_postal="", site_web_entreprise="", couleur="", id_evenement='', id_user=''):
        
        self.id = id
        self.identite_investisseur = identite_investisseur
        self.personnalite_juridique = personnalite_juridique
        self.nom_entreprise = nom_entreprise
        self.qualification = qualification
        self.adresse_email = adresse_email
        self.telephone = telephone
        self.pays = pays
        self.adresse_entreprise = adresse_entreprise
        self.boite_postal = boite_postal
        self.site_web_entreprise = site_web_entreprise
        self.couleur = couleur
        self.id_evenement = id_evenement
        self.id_user = id_user

    def liste_investisseur(self):

        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT t1.id, identite_investisseur, nom_entreprise, qualification, couleur, t2.nom_evenement, t3.nom, t3.postnom FROM dbo.Investisseur t1
                    LEFT OUTER JOIN dbo.Evenement t2 ON t2.id = t1.id_evenement
                    LEFT OUTER JOIN dbo.Users t3 ON t3.id = t1.id_user;
            """)
            liste = cursor.fetchall()

        return liste
    
    def un_investisseur(self):

        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT id, identite_investisseur, qualification, nom_entreprise, adresse_email, telephone, site_web_entreprise, pays, adresse_entreprise, boite_postal, couleur
                        FROM dbo.Investisseur WHERE id = %s; """, [str(self.id)])
            investisseur = cursor.fetchone()

        return investisseur
    
    def ajouter_investisseur(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Investisseur (identite_investisseur, personnalite_juridique, nom_entreprise, qualification, adresse_email, telephone, pays, adresse_entreprise, boite_postal, site_web_entreprise, couleur, id_evenement, id_user)
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, [
                    self.identite_investisseur,
                    self.personnalite_juridique,
                    self.nom_entreprise,
                    self.qualification,
                    self.adresse_email,
                    self.telephone,
                    self.pays,
                    self.adresse_entreprise,
                    self.boite_postal,
                    self.site_web_entreprise,
                    self.couleur,
                    str(self.id_evenement),
                    str(self.id_user)
                ])
            return True
        except Exception as e:
            print("Erreur lors de l'insertion de l'investisseur :", e)
            return False

    def delete_investisseur(self):

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM dbo.Investisseur WHERE id = %s", [ self.id ])

                return True
            
        except Exception as e:
            print("Erreur lors de la suppression de l'investisseur :", e)
            return False

    def update_investisseur(self):

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                        UPDATE dbo.Investisseur
                        SET identite_investisseur = %s, nom_entreprise = %s, qualification = %s, adresse_email = %s, telephone = %s, pays = %s, adresse_entreprise = %s, boite_postal = %s, site_web_entreprise = %s, couleur = %s
                        WHERE id = %s
                    """, [self.identite_investisseur,
                          self.nom_entreprise,
                          self.qualification,
                          self.adresse_email,
                          self.telephone,
                          self.pays,
                          self.adresse_entreprise,
                          self.boite_postal,
                          self.site_web_entreprise,
                          self.couleur,
                          str(self.id)])
            return True
        except Exception as e:
            print("Erreur lors de l UPDATE de l'investisseur :", e)
            return False
