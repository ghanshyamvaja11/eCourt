# Generated by Django 5.0.7 on 2025-01-13 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='case',
            old_name='laywer_accepted',
            new_name='lawyer_accepted',
        ),
    ]
