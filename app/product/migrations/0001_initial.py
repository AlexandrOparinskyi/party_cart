# Generated by Django 5.1.4 on 2024-12-28 08:04

import autoslug.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=150)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sale', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('image1', models.ImageField(upload_to='products_image')),
                ('image2', models.ImageField(null=True, upload_to='products_image')),
                ('image3', models.ImageField(null=True, upload_to='products_image')),
                ('category', models.ForeignKey(default='Products', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='products', to='product.category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]