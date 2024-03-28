# Generated by Django 4.2.1 on 2024-01-28 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_doubts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lsp_username', models.CharField(max_length=100)),
                ('client_username', models.CharField(max_length=100)),
                ('message_type', models.CharField(max_length=50)),
                ('case_description', models.TextField()),
            ],
        ),
    ]