# Generated by Django 5.0 on 2024-01-09 12:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_carouselfigure"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.CharField(
                default="https://ai-media.xiazq.com/media/avatar.jpg",
                max_length=100,
                verbose_name="头像",
            ),
        ),
    ]