# Generated by Django 2.0.3 on 2018-09-29 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Assignment', '0002_auto_20180929_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textentry',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='textdata', to=settings.AUTH_USER_MODEL),
        ),
    ]
