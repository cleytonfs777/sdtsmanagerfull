# Generated by Django 4.2.4 on 2023-12-02 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0017_remove_pacoteaquisicaoequipamentoservico_pacotedespesa_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dotacaoorcamentaria',
            name='data',
            field=models.DateField(blank=True, null=True),
        ),
    ]