# Generated by Django 4.2 on 2024-08-20 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cash',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
