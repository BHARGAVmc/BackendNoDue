# Generated by Django 5.2.3 on 2025-07-12 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fdetailsdash', '0002_remove_subject_class_section_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentrequirementstatus',
            name='certificate_file',
            field=models.FileField(blank=True, null=True, upload_to='certificates/'),
        ),
    ]
