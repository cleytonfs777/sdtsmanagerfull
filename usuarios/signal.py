from django.db.models.signals import post_save
from django.dispatch import receiver
from rolepermissions.roles import assign_role

from .models import Usuario


@receiver(post_save, sender=Usuario)
def define_permissoes(sender, instance, created, **kwargs):
    if created:
        if instance.cargo == "A":
            assign_role(instance, 'administrador')
        elif instance.cargo == "G":
            assign_role(instance, 'gerente')
        elif instance.cargo == "U":
            assign_role(instance, 'usuario')
