from django.db import connection
from django.db import transaction

class Investissement():
    def __init__(self, id_invest='', date_de_demande="", objet="", secteur="", id_investisseur='', id_suivi_relation=0, statut="", couleur="", source="", derniere_interaction="", prochaine_etape="", id_indicateur_cle=0, commentair="", taux_progretion=0, fk_id_investissement=0):
        self.id_invest = id_invest
        self.date_de_demande = date_de_demande
        self.objet = objet
        self.secteur = secteur
        self.id_investisseur = id_investisseur
        self.id_suivi_relation = id_suivi_relation
        self.statut = statut
        self.couleur = couleur
        self.source = source
        self.derniere_interaction = derniere_interaction
        self.prochaine_etape = prochaine_etape
        self.id_indicateur_cle = id_indicateur_cle
        self.commentair = commentair
        self.taux_progretion = taux_progretion
        self.fk_id_investissement = fk_id_investissement

    def liste_investissement(self):

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT t1.id, t1.date_de_demande, t1.objet, t1.secteur, t2.statut, t2.source, t2.derniere_interaction, t2.prochaine_etape, t3.commentair, t3.taux_progretion
                FROM dbo.Investissement t1
                LEFT OUTER JOIN dbo.Suivi_relation t2 ON t1.id = t2.id_investissemment
                LEFT OUTER JOIN dbo.Indicateur_cle t3 ON t1.id = t3.id_investissemment
                WHERE t1.id_investisseur = %s;
            """, [str(self.id_investisseur)])
            liste = cursor.fetchall()

        return liste
    
    def un_investissement(self):

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT t1.id, t1.date_de_demande, t1.objet, t1.secteur, t2.statut, t2.source, t2.derniere_interaction, t2.prochaine_etape, t3.commentair, t3.taux_progretion
                FROM dbo.Investissement t1
                LEFT OUTER JOIN dbo.Suivi_relation t2 ON t1.id = t2.id_investissemment
                LEFT OUTER JOIN dbo.Indicateur_cle t3 ON t1.id = t3.id_investissemment
                WHERE t1.id = %s;
            """, [str(self.id_invest)])
            liste = cursor.fetchone()

        return liste
    
    def nouveau_investissement(self):
        
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO dbo.Investissement (date_de_demande, objet, secteur, id_investisseur) OUTPUT INSERTED.id
                        VALUES (%s, %s, %s, %s);
                    """, [
                        self.date_de_demande,
                        self.objet,
                        self.secteur,
                        str(self.id_investisseur)
                    ])
                    
                    last_id = cursor.fetchone()[0]  # Récupérer l'ID de

                    print("id voiici l idi --------->>>>>>>>",last_id)

                    cursor.execute("""
                        INSERT INTO dbo.Suivi_relation (statut, source, derniere_interaction, prochaine_etape, id_investissemment)
                        VALUES (%s, %s, %s, %s, %s)
                    """, [
                        self.statut,
                        self.source,
                        self.derniere_interaction,
                        self.prochaine_etape,
                        str(last_id)
                    ])

                    cursor.execute("""
                        INSERT INTO dbo.Indicateur_cle (commentair, taux_progretion, id_investissemment)
                        VALUES (%s, %s, %s)
                    """, [
                        self.commentair,
                        self.taux_progretion,
                        str(last_id)
                    ])
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'investissement : {e}")
            return False
        
    def update_investissement(self):
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(""" 
                        UPDATE dbo.Investissement
                        SET date_de_demande = %s, objet = %s, secteur = %s
                        WHERE id = %s;
                    """, [self.date_de_demande, self.objet, self.secteur, str(self.id_invest)])

                    cursor.execute("""
                        UPDATE dbo.Suivi_relation
                        SET statut = %s, source = %s, derniere_interaction = %s,  prochaine_etape = %s
                        WHERE id_investissemment = %s;
                    """, [self.statut, self.source, self.derniere_interaction, self.prochaine_etape, str(self.id_invest)])

                    cursor.execute("""
                        UPDATE dbo.Indicateur_cle
                        SET commentair = %s, taux_progretion = %s
                        WHERE id_investissemment = %s;
                    """, [self.commentair, self.taux_progretion, str(self.id_invest)])
                return True
        except Exception as e:
            print(f"Erreur lors de l'UPDATE de l'investissement : {e}")
            return False
