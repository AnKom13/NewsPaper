# Generated by Django 4.2.4 on 2023-08-08 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_category_name_en_us_category_name_ru'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='heading_en_us',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Заголовок'),
        ),
        migrations.AddField(
            model_name='post',
            name='heading_ru',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Заголовок'),
        ),
    ]