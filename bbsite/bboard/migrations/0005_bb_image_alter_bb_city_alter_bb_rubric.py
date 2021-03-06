# Generated by Django 4.0.5 on 2022-07-20 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0004_city_bb_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='bb',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Фотография'),
        ),
        migrations.AlterField(
            model_name='bb',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bbs', to='bboard.city', verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='bb',
            name='rubric',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bbs', to='bboard.rubric', verbose_name='Рубрика'),
        ),
    ]
