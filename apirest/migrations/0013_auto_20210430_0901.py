# Generated by Django 3.1.7 on 2021-04-30 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apirest', '0012_auto_20210430_0054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artista',
            old_name='self_artist',
            new_name='self',
        ),
    ]
