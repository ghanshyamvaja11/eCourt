# Generated by Django 5.0.7 on 2024-12-31 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_number', models.CharField(max_length=50, unique=True)),
                ('case_title', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACTIVE', 'Active'), ('DISMISSED', 'Dismissed'), ('CLOSED', 'Closed')], default='PENDING', max_length=20)),
                ('case_filed_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='documents/%Y/%m/%d/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hearing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=100)),
                ('outcome', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
