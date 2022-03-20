# Generated by Django 3.2.8 on 2022-03-20 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_friendrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='address',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='pet',
            name='bio',
            field=models.TextField(blank=True, default='no bio...', max_length=100),
        ),
        migrations.AlterField(
            model_name='pet_lover',
            name='address',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='pet_lover',
            name='bio',
            field=models.TextField(blank=True, default='no bio...', max_length=100),
        ),
        migrations.AlterField(
            model_name='store',
            name='address',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='store',
            name='bio',
            field=models.TextField(blank=True, default='no bio...', max_length=100),
        ),
        migrations.AlterField(
            model_name='veterinarian',
            name='address',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='veterinarian',
            name='bio',
            field=models.TextField(blank=True, default='no bio...', max_length=100),
        ),
    ]