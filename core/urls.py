
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('projetos/', include('projetos.urls')),
    path('radiocom/', include('radiocom.urls')),
]
