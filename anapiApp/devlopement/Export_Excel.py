from django.http import HttpResponse

from .EvenementM import list_event, un_event

from openpyxl import Workbook
from datetime import datetime
from django.db import connection
import re


def safe_sheet_title(title):
    # Supprimer les caractères interdits par Excel
    title = re.sub(r'[\\/*?:\[\]]', '-', title)

    # Limiter à 31 caractères (règle Excel)
    return title[:31]

def export_excel_file():
    try:
        workbook = Workbook()

        feuil = list_event()

        with connection.cursor() as cursor:
            cursor.execute(""" SELECT t5.nom_evenement, t1.identite_investisseur, t1.qualification, t1.adresse_email, t1.telephone, t2.date_de_demande, t2.objet, t2.secteur, t1.pays, t3.statut, t3.source, t3.derniere_interaction, t3.prochaine_etape, t4.commentair, t4.taux_progretion
                FROM dbo.Investisseur t1
                LEFT OUTER JOIN dbo.Investissement t2 ON t1.id = t2.id_investisseur
                LEFT OUTER JOIN dbo.Suivi_relation t3 ON t2.id = t3.id_investissemment
                LEFT OUTER JOIN dbo.Indicateur_cle t4 ON t2.id = t4.id_investissemment
                RIGHT OUTER JOIN dbo.Evenement t5 ON t5.id = t1.id_evenement; 
            """)
            
            res = cursor.fetchall()

        sheets = {}

        for item in feuil:

            nom_evenement = item[1]

            ws = workbook.create_sheet(title=safe_sheet_title(item[1]))
            ws.append(["Evenement", "Identite de l' investiseur", "Qualification", "Adrresse E mail", "Telephone", "Date de demande", "Objet",
                      "Secteur", "Pays", "Statut", "Source", "Dernier Interaction", "Prochaine etape", "Commentair", "Taux de progretion"])
            
            sheets[nom_evenement] = ws
        
        if not res:
            print("Aucune donnee SQL trouver")
        else:
            for row in res:
                nom_evenement = row[0]

                ws = sheets.get(nom_evenement)

                if ws:
                    ws.append(list(row))

        date = datetime.now().strftime("%Y%m%d%H%M%S")

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response[
            'Content-Disposition'] = f'attachment; filename=fiche_de_suivi_de_l_investisseur[{date}].xlsx'
        workbook.save(response)
        return response

    except Exception as e:
        return HttpResponse(f"Erreur lors de la generation du fichier Exel : {e}", status=500)
