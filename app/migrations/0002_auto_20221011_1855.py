# Generated by Django 3.1.7 on 2022-10-11 18:55

from django.db import migrations, models
import ulid.api.api


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default=ulid.api.api.Api.new, editable=False, max_length=32, primary_key=True, serialize=False, unique=True),
        ),
    ]