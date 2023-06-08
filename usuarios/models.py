from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    choices_cargo = (('A', 'Administrador'),
                     ('G', 'Gerente'), ('U', 'Usuário'))

    cargo = models.CharField(max_length=1, choices=choices_cargo, default='U')
