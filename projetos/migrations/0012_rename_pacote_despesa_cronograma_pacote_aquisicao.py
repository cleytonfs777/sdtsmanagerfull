# Generated by Django 4.2.1 on 2023-07-05 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0011_remove_equipamentoservico_tipo_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cronograma',
            old_name='pacote_despesa',
            new_name='pacote_aquisicao',
        ),
    ]
