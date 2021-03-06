# Generated by Django 4.0.5 on 2022-07-20 11:56

import bboard.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0006_alter_bb_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(db_index=True, max_length=150, validators=[bboard.models.accept_city], verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='rubric',
            name='name',
            field=models.CharField(db_index=True, max_length=20, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='Название'),
        ),
    ]
