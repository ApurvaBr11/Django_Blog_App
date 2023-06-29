# Generated by Django 4.2.1 on 2023-06-24 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sms', '0008_notes_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='f_by', to=settings.AUTH_USER_MODEL)),
                ('followed_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='f_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
