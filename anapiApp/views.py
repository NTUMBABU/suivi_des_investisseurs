
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

from django.db import connection

from datetime import datetime

from .devlopement.Investisseur import Investisseur
from .devlopement.Investissement import Investissement
from .devlopement.EvenementM import list_event, add_event, un_event
from .devlopement.Export_Excel import export_excel_file
from .devlopement.session_login import session_login_required


def connexion(request):
    if request.method == 'GET':
        template = loader.get_template('connexion.html')
        return HttpResponse(template.render({}, request))
    
    elif request.method == "POST":
        nom = request.POST.get('name', '').strip()
        email = request.POST.get('email', '')

        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT *
                           FROM dbo.Users
                           WHERE CAST(nom AS varchar) = %s 
                           AND CAST(email AS varchar) = %s
                           """,[nom, email])
            row = cursor.fetchone()
        
        if row is None:
            messages.error(request, "Utilisateur introuvable.")
            return redirect('connexion')

        user_id = row[0]
        username = row[1]
        email_user = row[5]

        request.session['utilisateur_id'] = str(user_id)
        request.session['utilisateur_nom'] = username
        request.session['utilisateur_postnom'] = row[2]
        request.session['utilisateur_prenom'] = row[3]
        request.session['utilisateur_email'] = email_user

        request.session.set_expiry(60 * 60 * 8)  # 8 heures

        messages.success(request, f"Bienvenue {nom} !")
        return redirect('home')

def inscription(request):
    if request.method == 'GET':
        template = loader.get_template('inscription.html')
        return HttpResponse(template.render({}, request))

    elif request.method == "POST":
        nom = request.POST.get('nom_ins')
        postNom = request.POST.get('postNom')
        prenom = request.POST.get('prenom')
        sexe = request.POST.get('sexe')
        email = request.POST.get('email')

        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT * FROM dbo.Users
                        WHERE CAST(email AS varchar) = %s
            """, [email])
            row = cursor.fetchone()

        if row is not None:
            messages.error(request, "Utilisateur exite déjà !")
            return redirect('inscription')
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                                INSERT INTO Users (nom, postnom, prenom, sex, email)
                                VALUES
                                (%s, %s, %s, %s, %s);
                    """, [nom, postNom, prenom, sexe, email])
                messages.success(request, "Compte créé avec succès.")
                return redirect('connexion')
            except Exception as e:
                print(f"Erreur lors de l'insertion de l'utilisateur : {e}")
                messages.error(
                    request, "Erreur lors de l'insertion de l'utilisateur !!!")
                return redirect('inscription')


def deconnexion(request):
    request.session.flush()
    return redirect('connexion')

def export_excel(request):
    return export_excel_file()

@csrf_protect
def new_event(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        res = add_event(nom)
        if res == True:
            messages.success(request, "Evenement ajouté avec succès !")
            return redirect('home')
        else:
            messages.error(request, "Erreur lors de l'ajout de l'evenement.")
            template = loader.get_template('index.html')
            return HttpResponse(template.render({}, request))


@session_login_required
def update_investissement(request, invest_id, investisseur_id):
    if request.method == 'GET':
        invest = Investissement(id_invest=invest_id)
        invest = invest.un_investissement()

        context = {'investissement': invest, 'investisseur': investisseur_id}

        template = loader.get_template('update_investissement.html')
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        date_de_demande = request.POST.get('date_de_demande')
        objet = request.POST.get('objet')
        secteur = request.POST.get('secteur')
        ###
        statut = request.POST.get('statut')
        source = request.POST.get('source')
        derniere_interaction = request.POST.get('derniere_interaction')
        prochaine_etape = request.POST.get('prochaine_etape')
        ###
        commentair = request.POST.get('commentair')
        taux_progretion = request.POST.get('taux')

        invest = Investissement(id_invest=invest_id, date_de_demande=date_de_demande, objet=objet, secteur=secteur, statut=statut, source=source, derniere_interaction=derniere_interaction, prochaine_etape=prochaine_etape, commentair=commentair, taux_progretion=taux_progretion)

        res = invest.update_investissement()

        if res == True:
            messages.success(request, "Investissement mis à jour avec succès !")
            return redirect('detail_investisseur', investisseur_id=investisseur_id)
        else:
            invest = Investissement(id_invest=invest_id)
            invest = invest.un_investissement()
            context = {'investissement': invest}

            messages.error(request, "Erreur lors de la mis à jour de l'investissement. Veuillez vérifier les informations et réessayer.")
            template = loader.get_template('update_investissement.html')
            return HttpResponse(template.render(context, request))


def new_investissement(request, invest_id):
    if request.method == 'POST':
        date_de_demande = request.POST.get('date_de_demande')
        objet = request.POST.get('objet')
        secteur = request.POST.get('secteur')
        ###
        statut = request.POST.get('statut')
        source = request.POST.get('source')
        derniere_interaction = request.POST.get('derniere_interaction')
        prochaine_etape = request.POST.get('prochaine_etape')
        ###
        commentair = request.POST.get('commentair')
        taux_progretion = request.POST.get('taux')

        investissement = Investissement(date_de_demande=date_de_demande, objet=objet, secteur=secteur, id_investisseur=invest_id, statut=statut, source=source,
                    derniere_interaction=derniere_interaction, prochaine_etape=prochaine_etape, commentair=commentair, taux_progretion=taux_progretion)

        res = investissement.nouveau_investissement()

        if res == True:
            messages.success(request, "Investissement ajouté avec succès !")
            return redirect('detail_investisseur', investisseur_id=invest_id)
        else:
            messages.error(
                request, "Erreur lors de l'ajout de l'investissement. Veuillez vérifier les informations et réessayer.")
            template = loader.get_template('new_investissement.html')
            return HttpResponse(template.render({'invest_id': invest_id}, request))

    elif request.method == 'GET':
        investisseur = Investisseur(id=invest_id)
        investisseur = investisseur.un_investisseur()

        template = loader.get_template('new_investissement.html')
        return HttpResponse(template.render({'invest_id': invest_id, 'investisseur': investisseur, 'dateActual': datetime.now().strftime("%Y-%m-%d")}, request))


def new_investisseur(request):
    if request.method == 'POST':
        identite_investisseur = request.POST.get('identite_investisseur')
        personalite_juridique = 'NaN'
        nom_entreprise = request.POST.get('nom_entreprise')
        qualification = request.POST.get('qualification')
        ###
        adresse_email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        site_web_entreprise = request.POST.get('site_web')
        ###
        pays = request.POST.get('pays')
        adresse_entreprise = request.POST.get('adresse_entreprise')
        boite_postal = request.POST.get('boite_postal')
        ###
        couleur = request.POST.get('couleur')
        event = request.POST.get('evenement')

        investisseur = Investisseur(identite_investisseur=identite_investisseur, personnalite_juridique=personalite_juridique, nom_entreprise=nom_entreprise, qualification=qualification, adresse_email=adresse_email,
                                    telephone=telephone, pays=pays, adresse_entreprise=adresse_entreprise, boite_postal=boite_postal, site_web_entreprise=site_web_entreprise, couleur=couleur, id_evenement=event, id_user=request.session['utilisateur_id'])

        res = investisseur.ajouter_investisseur()

        if res == True:
            messages.success(request, "Investisseur ajouté avec succès !")
            return redirect('home')  # Assurez-vous que le nom de l'URL pour la page d'accueil est bien 'home' dans vos urls.py
        else:
            messages.error(request, "Erreur lors de l'ajout de l'investisseur. Veuillez vérifier les informations et réessayer.")
            template = loader.get_template('new_investisseur.html')
            return HttpResponse(template.render({}, request))
    
    elif request.method == 'GET':
        liste_Evenement = list_event()
        template = loader.get_template('new_investisseur.html')
        return HttpResponse(template.render({'event': liste_Evenement}, request))
    
    elif request.method == 'PUT':
        pass

@csrf_protect
def remove_investisseur(request):
    if request.method == 'POST':
        
        investisseur_id = request.POST.get('id')
        investisseur = Investisseur(id=investisseur_id)
        res = investisseur.delete_investisseur()
        if res == True:
            return JsonResponse({"status": 'Success!', 'message': "Suppression avec succès !"})
        else:
            return JsonResponse({"status": 'Echec!', 'message': "Erreur de suppression."})


@session_login_required
def detail_investisseur(request, investisseur_id):
    investisseur = Investisseur(id=investisseur_id)
    investisseur = investisseur.un_investisseur()

    liste_investissement = Investissement(id_investisseur=investisseur_id)
    liste_investissement = liste_investissement.liste_investissement()

    template = loader.get_template('detail_investisseur.html')
    return HttpResponse(template.render({'investisseur': investisseur, 'investissements': liste_investissement}, request))


@csrf_protect
def update_investisseur(request, investisseurUP_id):
    if request.method == 'GET':
        liste_Evenement = list_event()

        investisseur = Investisseur(id=investisseurUP_id)
        investisseur = investisseur.un_investisseur()

        un_evenement = un_event(investisseurUP_id)

        context = {
            'event': liste_Evenement,
            'un_event': un_evenement,
            'investisseur': investisseur, 
            'id_invest': investisseurUP_id
        }

        template = loader.get_template('update_investisseur.html')
        return HttpResponse(template.render(context, request))
    
    elif request.method == 'POST':
        identite_investisseur = request.POST.get('identite_investisseur')
        personalite_juridique = 'NaN'
        nom_entreprise = request.POST.get('nom_entreprise')
        qualification = request.POST.get('qualification')
        ###
        adresse_email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        site_web_entreprise = request.POST.get('site_web')
        ###
        pays = request.POST.get('pays')
        adresse_entreprise = request.POST.get('adresse_entreprise')
        boite_postal = request.POST.get('boite_postal')
        ###
        couleur = request.POST.get('couleur')
        event = request.POST.get('evenement')
        
        investisseur = Investisseur(id=investisseurUP_id, identite_investisseur=identite_investisseur, personnalite_juridique=personalite_juridique, nom_entreprise=nom_entreprise, qualification=qualification, adresse_email=adresse_email, telephone=telephone, pays=pays, adresse_entreprise=adresse_entreprise, boite_postal=boite_postal, site_web_entreprise=site_web_entreprise, couleur=couleur, id_evenement=event)

        res = investisseur.update_investisseur()

        if res == True:
            messages.success(request, "Investisseur Modifier avec succès !")
            return redirect('home')
        else:
            liste_Evenement = list_event()
            investisseur = Investisseur(id=investisseurUP_id)
            investisseur = investisseur.un_investisseur()

            context = {
                'event': liste_Evenement,
                'investisseur': investisseur,
                'id_invest': investisseurUP_id
            }
            messages.error(request, "Erreur lors de la de la modification. Veuillez vérifier les informations et réessayer.")
            template = loader.get_template('update_investisseur.html')
            return HttpResponse(template.render(context, request))


@session_login_required
def home(request):
    listeInvestisseur = Investisseur()
    res = listeInvestisseur.liste_investisseur()
    liste_Evenement = list_event()
    
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'indicateurs': res, 'event': liste_Evenement}, request))

# python manage.py runserver
