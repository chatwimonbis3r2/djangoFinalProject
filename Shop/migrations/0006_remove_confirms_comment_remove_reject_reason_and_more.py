# Generated by Django 4.1.6 on 2023-02-24 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0005_orders_transfers_send_reject_orderdetails_confirms_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='confirms',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='reject',
            name='reason',
        ),
        migrations.RemoveField(
            model_name='transfers',
            name='comment',
        ),
    ]