# Generated by Django 4.0.3 on 2022-03-09 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelTable(
            name='comment',
            table='Comments ',
        ),
    ]
