# Generated by Django 5.0.2 on 2024-12-09 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_newuser_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='code',
            field=models.CharField(default='ZV5G4_1733740112_K1FEB', max_length=150),
        ),
    ]
