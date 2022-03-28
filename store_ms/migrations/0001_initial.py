# Generated by Django 3.1.14 on 2022-03-24 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('IsVeg', models.BooleanField(default=True)),
                ('price', models.IntegerField()),
                ('thumbnail', models.CharField(max_length=50)),
                ('itemRating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('itemRatingCount', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locLatitude', models.DecimalField(decimal_places=3, max_digits=8)),
                ('locLongitude', models.DecimalField(decimal_places=3, max_digits=8)),
                ('address', models.TextField()),
                ('name', models.CharField(max_length=50)),
                ('availabilityTime', models.CharField(max_length=50)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('ratingCount', models.IntegerField(default=1)),
                ('contactInfo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StoreRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('storeId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.store')),
            ],
        ),
        migrations.CreateModel(
            name='StoreMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.item')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.store')),
            ],
        ),
        migrations.AddField(
            model_name='store',
            name='menu',
            field=models.ManyToManyField(related_name='stores', through='store.StoreMenu', to='store.Item'),
        ),
        migrations.CreateModel(
            name='ItemRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('itemId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.item')),
            ],
        ),
    ]