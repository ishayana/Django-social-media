# Generated by Django 4.2.5 on 2024-04-12 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_blogmodel_created_blogimagemodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogmodel',
            name='image',
        ),
    ]
