# Generated by Django 4.2.1 on 2023-06-14 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0004_remove_pacotedespesa_beneficiado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pacotedespesa',
            name='pacotereceita',
        ),
    ]
