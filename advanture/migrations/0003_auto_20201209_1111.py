# Generated by Django 2.2.5 on 2020-12-09 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advanture', '0002_advanture_comment_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='rentalad',
            new_name='advanture',
        ),
        migrations.RenameField(
            model_name='images',
            old_name='rentalad',
            new_name='advanture',
        ),
    ]
