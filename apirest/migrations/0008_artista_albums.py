# Generated by Django 3.1.7 on 2021-04-29 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apirest', '0007_remove_artista_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='artista',
            name='albums',
            field=models.URLField(blank=True, default='/apirest/<django.db.models.fields.CharField>'),
        ),
    ]
