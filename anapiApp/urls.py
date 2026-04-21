from django.urls import path
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    path('service-worker.js', TemplateView.as_view(template_name="service-worker.js",content_type="application/javascript",),),

    path('', views.home, name='home'),
    path('investisseur/<uuid:investisseur_id>/', views.detail_investisseur, name='detail_investisseur'),
    path('nouvel-investissement/<uuid:invest_id>/', views.new_investissement, name='new_investissement'),
     
    path('nouvel-investisseur/', views.new_investisseur, name='new_investisseur'),
    path('update-investisseur/<uuid:investisseurUP_id>/', views.update_investisseur, name='update_investisseur'),
    path('delete_investisseur/', views.remove_investisseur, name='remove_investisseur'),

    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

    path('export-excel/', views.export_excel, name='export_excel'),
    path('update-investissement/<uuid:investisseur_id>/<uuid:invest_id>/', views.update_investissement, name='update_investissement'),
    path('new-event/', views.new_event, name='new_event'),
]