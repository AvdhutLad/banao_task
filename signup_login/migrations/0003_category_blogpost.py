# Generated by Django 5.0 on 2024-09-02 04:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup_login', '0002_alter_user_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(default='', upload_to='blog_images/')),
                ('summary', models.TextField(max_length=300)),
                ('content', models.TextField()),
                ('is_draft', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to='signup_login.user')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to='signup_login.category')),
            ],
        ),
    ]
