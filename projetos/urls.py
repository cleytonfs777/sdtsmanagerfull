from django.urls import path

from . import views

urlpatterns = [
    path('painel/', views.painel, name='painel'),
    path('painel/project/<int:id_project>', views.project, name='project'),
    path('painel/project/newpackageaqu/<int:id_project>/',
         views.newpackageaqu, name='newpackageaqu'),
    path('painel/project/newpackageaqu/createequipserv/<int:id_project>/',
         views.createequipserv, name='createequipserv'),
    path('painel/project/pacoteedit/createequipserv_edit<int:id_pacote>/',
         views.createequipserv_edit, name='createequipserv_edit'),
    path('painel/project/createpackage/<int:id_project>',
         views.createpackage, name='createpackage'),
    path('painel/project/pacoteedit/<int:id_pacote>',
         views.pacoteedit, name='pacoteedit'),
    path('painel/project/pacoteedit/createfullequip/<int:id_pacote>',
         views.createfullequip, name='createfullequip'),
    path('painel/project/allservpack/<int:id_element>',
         views.allservpack, name='allservpack'),
    path('painel/project/deleteequip/<int:id_element>',
         views.deleteequip, name='deleteequip'),
    path('painel/project/pacoteview/<int:id_pacote>',
         views.pacoteview, name='pacoteview'),
    path('painel/project/newprojectrecet',
         views.newprojectrecet, name='newprojectrecet'),
]
