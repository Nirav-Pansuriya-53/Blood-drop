# Generated by Django 4.1.7 on 2023-03-31 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbank', '0002_alter_donation_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='donation_date',
            field=models.DateTimeField(),
        ),
    ]
