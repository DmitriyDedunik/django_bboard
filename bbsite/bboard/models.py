"""Describe project models."""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models


def accept_city(city):
    if city not in {'Москва', 'Санкт-Петербург'}:
        raise ValidationError('Такой город не разрешен!')


class Bb(models.Model):
    """Describe form by Bb model."""

    max_length = 50
    title = models.CharField(
        max_length=max_length,
        verbose_name='Наименование',
        help_text='Name',
    )
    content = models.TextField(  # noqa: WPS110
        null=True,
        blank=True,
        verbose_name='Описание',
        db_column='content',
    )
    price = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Цена',
        default=0,
        validators=[MinValueValidator(0)],
    )
    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации',
    )
    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Рубрика',
        related_name='bbs',
    )
    city = models.ForeignKey(
        'City',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Город',
        related_name='bbs',
    )
    image = models.ImageField(
        upload_to='images',
        verbose_name='Фотография',
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        verbose_name='Пользователь',
        blank=True,
        null=True,
    )

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
        max_length=max_length,
        verbose_name='Название',
        db_index=True,
        validators=[MinLengthValidator(3)],
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
        max_length=max_length,
        verbose_name='Название',
        db_index=True,
        validators=[accept_city],
    )

    class Meta(object):
        """Describe form by City."""

        ordering = ['name']
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        """Return name of city.

        Returns:
            self.name - name of city.
        """
        return self.name

class Chat(models.Model):
    """Describe Chat model."""
    
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        verbose_name='От кого',
        related_name='chats_from',
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        verbose_name='Кому',
        related_name='chats_to',
    )
    message = models.TextField(
        verbose_name='Сообщение',
    )     
    bb = models.ForeignKey(
        'Bb',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Объявление',
        related_name='messages',
    )
    dt = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата сообщения',
    )

    class Meta:
        """Describe form by Chat."""

        ordering = ('-dt',)
