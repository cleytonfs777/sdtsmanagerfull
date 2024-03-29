from django.urls import path

from . import views

urlpatterns = [
     path('painel/', views.painel, name='painel'),
     # Funçõe e URLs relacionadas a projetos
     path('painel/project/<int:id_project>', views.project, name='project'),
     path('painel/project/deleteproject/<int:id_project>',
          views.deleteproject, name='deleteproject'),
     path('painel/project/editproject/<int:id_project>',
               views.editproject, name='editproject'),
     path('painel/project/newprojectrecet',
          views.newprojectrecet, name='newprojectrecet'),

     # Funçõe e URLs relacionadas a pacotes de aquisição de projetos
     path('painel/project/newpackageaqu/<int:id_project>/',
          views.newpackageaqu, name='newpackageaqu'),
     path('painel/project/createpackage/<int:id_project>',
          views.createpackage, name='createpackage'),
     path('painel/project/pacoteedit/<int:id_pacote>',
          views.pacoteedit, name='pacoteedit'),
     path('painel/project/removepackage/<int:id_pacote>',
          views.removepackage, name='removepackage'),
     path('painel/project/allservpack/<int:id_element>',
          views.allservpack, name='allservpack'),
     path('painel/project/pacoteview/<int:id_pacote>',
          views.pacoteview, name='pacoteview'),

     # Funçõe e URLs relacionadas a Pacotes de Receita/Despesa
     path('painel/project/createpackagedesprec/<int:id_project>/',
          views.createpackagedesprec, name='createpackagedesprec'),
     path('painel/project/newpackagerec/<int:id_project>/',
          views.newpackagerec, name='newpackagerec'),
     path('painel/project/newpackagerec/createedotorc/<int:id_pacote_emp>/',
          views.createedotorc, name='createedotorc'),

     # Funçõe e URLs relacionadas a Equipamentos e Serviços
     path('painel/project/newpackageaqu/createequipserv/<int:id_project>/',
          views.createequipserv, name='createequipserv'),
     path('painel/project/pacoteedit/createequipserv_edit<int:id_pacote>/',
          views.createequipserv_edit, name='createequipserv_edit'),
     path('painel/project/deleteequip/<int:id_element>',
          views.deleteequip, name='deleteequip'),
     path('painel/project/pacoteedit/createfullequip/<int:id_pacote>',
          views.createfullequip, name='createfullequip'),
     # Funçõe e URLs relacionadas a Cronograma
     path('painel/project/pacoteedit/createtaskfull/<int:id_pacote>/',
          views.createtaskfull, name='createtaskfull'),
     path('painel/project/pacoteedit/deletetask/<int:id_task>/',
          views.deletetask, name='deletetask'),
     path('painel/project/pacoteedit/editeachtask/<int:id_task>/',
          views.editeachtask, name='editeachtask'),
     # Funções e URLs relacionadas a Observações e Pendencias
     path('painel/project/pacoteedit/createobspenfull/<int:id_pacote>/',
          views.createobspenfull, name='createobspenfull'),
     path('painel/project/pacoteedit/deleteobspen/<int:id_obspen>/',
          views.deleteobspen, name='deleteobspen'),
     path('painel/project/pacoteedit/editobspen/<int:id_obspen>/',
          views.editobspen, name='editobspen'),


]
