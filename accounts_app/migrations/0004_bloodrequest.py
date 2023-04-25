# Generated by Django 3.2.18 on 2023-04-21 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0003_user_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('blood_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bloodrequest', to='accounts_app.bloodgroup')),
                ('bloodbank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blood_requests', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
