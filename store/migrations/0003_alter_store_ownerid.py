# Generated by Django 4.0.3 on 2022-03-29 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_store_ownerid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='ownerId',
            field=models.IntegerField(),
        ),
    ]