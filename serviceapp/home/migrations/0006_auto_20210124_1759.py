# Generated by Django 2.2.5 on 2021-01-24 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20210124_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='speciality',
            field=models.ForeignKey(db_column='SPECIALITY', default='', on_delete=django.db.models.deletion.CASCADE, to='home.Service'),
        ),
    ]