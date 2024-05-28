# Generated by Django 5.0.4 on 2024-04-29 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_userprofile_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='user_friends', to='myapp.userprofile'),
        ),
    ]