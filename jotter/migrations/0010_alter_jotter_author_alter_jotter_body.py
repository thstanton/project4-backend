# Generated by Django 4.2.7 on 2023-11-20 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jotter', '0009_alter_pupilclass_access_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jotter',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_jotters', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='jotter',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
