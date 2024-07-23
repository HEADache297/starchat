# Generated by Django 5.0.7 on 2024-07-23 11:24

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0012_alter_chatroom_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='group_name',
            field=models.CharField(blank=True, default=shortuuid.main.ShortUUID.uuid, max_length=128, unique=True),
        ),
    ]
