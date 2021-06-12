# Generated by Django 3.1.4 on 2021-05-31 15:39

from django.db import migrations, models
import file_upload.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=file_upload.models.user_directory_path)),
                ('name', models.CharField(max_length=20, verbose_name='name')),
                ('sec_key', models.CharField(max_length=200)),
            ],
        ),
    ]