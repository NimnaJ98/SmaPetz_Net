# Generated by Django 4.0.3 on 2022-09-19 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='store_type',
            field=models.CharField(blank=True, choices=[('PETSTORE', 'Pet Store'), ('PRODUCTSTORE', 'Pet Product Store')], max_length=50),
        ),
    ]