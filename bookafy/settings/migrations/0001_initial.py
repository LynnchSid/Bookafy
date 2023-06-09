# Generated by Django 4.1.7 on 2023-05-18 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=200)),
                ('logo', models.ImageField(upload_to='settings/logo')),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50, null=True)),
                ('state', models.CharField(max_length=50, null=True)),
                ('zipcode', models.CharField(max_length=50, null=True)),
                ('phone_no', models.CharField(max_length=20)),
                ('mobile_no', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('pan', models.CharField(max_length=50, null=True)),
                ('facebook', models.CharField(max_length=100)),
                ('instagram', models.CharField(max_length=100)),
                ('whatsapp', models.CharField(max_length=20)),
                ('about_description', models.CharField(max_length=255)),
                ('site_language', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
