# Generated by Django 4.1.7 on 2023-03-30 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='rate',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='rate',
            field=models.SmallIntegerField(default=0),
        ),
    ]
