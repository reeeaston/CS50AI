# Generated by Django 4.1.7 on 2023-08-10 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0004_post_user_user_followers_user_following_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]