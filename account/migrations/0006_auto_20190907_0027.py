# Generated by Django 2.1 on 2019-09-06 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20190907_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest_info',
            name='qr_code',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]