# Generated by Django 3.1.1 on 2024-05-21 11:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0007_auto_20240521_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=36, unique=True),
        ),
    ]