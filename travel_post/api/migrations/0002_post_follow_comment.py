# Generated by Django 4.1.3 on 2022-12-01 00:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=550)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('category', models.CharField(blank=True, default=None, max_length=225, null=True)),
                ('post_author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_post', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('followers', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='users_following', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='users_followed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1000)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.post')),
            ],
        ),
    ]
