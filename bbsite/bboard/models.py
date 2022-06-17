from importlib.resources import contents
from tabnanny import verbose
from turtle import title
from django.db import models


class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Наименование')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(
                            auto_now_add=True,
                            db_index=True,
                            verbose_name='Дата публикации',
                            )
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.SET_NULL, verbose_name='Рубрика')

    class Meta:
        ordering = ('-published',)
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class Rubric(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название', db_index=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'

    def __str__(self):
        return self.name
