# Generated by Django 4.1.6 on 2023-02-11 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='is_staff',
            new_name='is_admin',
        ),
    ]