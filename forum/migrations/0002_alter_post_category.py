# Generated by Django 3.2.16 on 2022-12-27 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.IntegerField(choices=[(0, 'Button'), (1, 'Navbar'), (2, 'Card'), (3, 'Miscellaneous')], default=3),
        ),
    ]