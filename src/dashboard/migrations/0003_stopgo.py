# Generated by Django 4.1.1 on 2022-09-29 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_statut'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stopgo',
            fields=[
                ('idStopgo', models.AutoField(primary_key=True, serialize=False)),
                ('statutStopgo', models.TextField()),
            ],
        ),
    ]
