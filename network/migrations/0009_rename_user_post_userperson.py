# Generated by Django 4.1.7 on 2023-08-10 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0008_user_followers_user_following"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post", old_name="user", new_name="userPerson",
        ),
    ]
