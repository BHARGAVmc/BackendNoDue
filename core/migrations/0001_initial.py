# Generated by Django 5.2.3 on 2025-07-08 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('role', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(default='student', max_length=10)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('roll_no', models.CharField(blank=True, max_length=20, null=True)),
                ('branch', models.CharField(blank=True, max_length=50, null=True)),
                ('year', models.CharField(blank=True, max_length=10, null=True)),
                ('sem', models.CharField(blank=True, max_length=10, null=True)),
                ('section', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FacultySubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=10)),
                ('semester', models.CharField(max_length=10)),
                ('section', models.CharField(max_length=10)),
                ('subject_code', models.CharField(max_length=20)),
                ('subject_name', models.CharField(max_length=100)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_mappings', to='core.faculty')),
            ],
            options={
                'unique_together': {('faculty', 'branch', 'year', 'semester', 'section', 'subject_code')},
            },
        ),
    ]
