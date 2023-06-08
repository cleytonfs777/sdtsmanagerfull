from django.urls import path

from . import views

urlpatterns = [
    path('painel/', views.painel, name='painel'),
    path('painel/project/', views.project, name='project'),
    path('painel/project/pacoteedit', views.pacoteedit, name='pacoteedit'),
    path('painel/project/pacoteview', views.pacoteview, name='pacoteview'),
    path('painel/project/newprojectrecet',
         views.newprojectrecet, name='newprojectrecet'),
]
