# Generated by Django 5.0.2 on 2024-04-04 06:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('website', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraphGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tree_structure', models.JSONField()),
                ('moves', models.IntegerField(default=0)),
                ('game_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.profile')),
            ],
        ),
    ]
