# Generated by Django 3.1.1 on 2024-05-07 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_listing_type'),
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='listing_id',
        ),
        migrations.AlterField(
            model_name='contact',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='listings.listing'),
        ),
    ]
