# Generated by Django 4.2.7 on 2023-11-17 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jotter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordbank',
            name='context',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='jotter.context'),
            preserve_default=False,
        ),
    ]
