# Generated by Django 3.2 on 2021-04-14 20:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tag', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('priority', models.CharField(choices=[('HIGHEST', 'HIGHEST'), ('HIGH', 'HIGH'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW'), ('LOWEST', 'LOWEST')], max_length=100)),
                ('is_completed', models.BooleanField(default=False)),
                ('tags', models.ManyToManyField(blank=True, to='tasks.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='task', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'task',
            },
        ),
    ]
