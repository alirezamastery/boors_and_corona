# Generated by Django 3.1.3 on 2020-11-19 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('path', models.CharField(max_length=512)),
            ],
        ),
        migrations.RemoveField(
            model_name='blockedip',
            name='api_name',
        ),
        migrations.CreateModel(
            name='SecurityConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.ManyToManyField(blank=True, related_name='config', to='guard.ViewDetail')),
            ],
        ),
    ]
