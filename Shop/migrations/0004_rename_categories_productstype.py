# Generated by Django 4.1.6 on 2023-02-22 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0003_categories_products'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='ProductsType',
        ),
    ]
