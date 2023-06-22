from django.urls import path

from . import views

urlpatterns = [
    path('painel/', views.painel, name='painel'),
    path('painel/project/<int:id_project>', views.project, name='project'),
    path('painel/project/newpackageaqu/<int:id_project>/',
         views.newpackageaqu, name='newpackageaqu'),
    path('painel/project/newpackageaqu/createequipserv/<int:id_project>/',
         views.createequipserv, name='createequipserv'),
    path('painel/project/createpackage/<int:id_project>',
         views.createpackage, name='createpackage'),
    path('painel/project/pacoteedit', views.pacoteedit, name='pacoteedit'),
    path('painel/project/pacoteview/<int:id_pacote>',
         views.pacoteview, name='pacoteview'),
    path('painel/project/newprojectrecet',
         views.newprojectrecet, name='newprojectrecet'),
]
