"""Describe project models."""
from django.db import models

from django.core.validators import MinValueValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.conf import settings

def accept_city(value):
    if value not in ['Москва', 'Санкт-Петербург']:
        raise ValidationError('Такой город не разрешен!')


class Bb(models.Model):
    """Describe form by Bb model."""

    title = models.CharField(max_length=50, verbose_name='Наименование', help_text='Name')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена', default=0, validators=[MinValueValidator(0)])
    published = models.DateTimeField(
                            auto_now_add=True,
                            db_index=True,
                            verbose_name='Дата публикации',
                            )
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.SET_NULL, verbose_name='Рубрика', related_name='bbs')
    city = models.ForeignKey('City', null=True, on_delete=models.SET_NULL, verbose_name='Город', related_name='bbs')
    image = models.ImageField(upload_to='images', verbose_name='Фотография', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, verbose_name='Пользователь', blank=True, null=True)

    class Meta(object):
        """Describe form by Bb."""
        
        ordering = ('-published',)
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class Rubric(models.Model):
    """Describe form by Rubric model."""

    max_length = 20
    name = models.CharField(
        max_length=max_length, verbose_name='Название',
        db_index=True, validators=[MinLengthValidator(3)],
    )

    class Meta(object):
        """Describe form by Rubric."""

        ordering = ['name']
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'

    def __str__(self):
        return self.name


class City(models.Model):
    """Describe City model."""

    max_length = 150
    name = models.CharField(
        max_length=max_length, verbose_name='Название',
        db_index=True, validators=[accept_city],
    )

    class Meta(object):
        """Describe form by City."""

        ordering = ['name']
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        """Describe return name form by City."""
        return self.name
