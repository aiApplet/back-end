# Generated by Django 5.0 on 2024-01-07 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselFigure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='carousel/', verbose_name='图片')),
                ('link', models.CharField(max_length=255, verbose_name='链接')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('sort', models.PositiveSmallIntegerField(default=0, verbose_name='排序')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图',
                'db_table': 'carousel_figure',
                'ordering': ['-sort', '-id'],
            },
        ),
    ]