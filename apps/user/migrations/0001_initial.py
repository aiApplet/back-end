# Generated by Django 5.0 on 2024-01-06 00:39

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupProxy',
            fields=[
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='PermissionProxy',
            fields=[
            ],
            options={
                'verbose_name': '权限',
                'verbose_name_plural': '权限',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.permission',),
            managers=[
                ('objects', django.contrib.auth.models.PermissionManager()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.CharField(default='https://ai.xiazq.com/media/avatar/avatar.jpg', max_length=100, verbose_name='头像')),
                ('nickname', models.CharField(max_length=100, verbose_name='微信昵称')),
                ('balance', models.PositiveIntegerField(default=0, verbose_name='余额')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'user',
                'ordering': ['-id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AccountRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='金额')),
                ('balance', models.PositiveIntegerField(verbose_name='余额')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('record_type', models.BooleanField(choices=[(True, '收入'), (False, '支出')], default=True, verbose_name='记录类型')),
                ('reward_type', models.PositiveSmallIntegerField(choices=[(0, '签到'), (1, '分享'), (2, '充值')], verbose_name='收支分类')),
                ('remark', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '账户记录',
                'verbose_name_plural': '账户记录',
                'db_table': 'account_record',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='RechargeableCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=20, unique=True, verbose_name='卡号')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='金额')),
                ('is_used', models.BooleanField(default=False, verbose_name='是否已使用')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('use_time', models.DateTimeField(blank=True, null=True, verbose_name='使用时间')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '充值卡',
                'verbose_name_plural': '充值卡',
                'db_table': 'rechargeable_card',
            },
        ),
        migrations.CreateModel(
            name='SignInDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='日期')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '签到日期',
                'verbose_name_plural': '签到日期',
                'db_table': 'sign_in_date',
                'ordering': ['-id'],
            },
        ),
    ]
