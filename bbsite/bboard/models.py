from importlib.resources import contents
from turtle import title
from django.db import models

class Bb(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    published = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-published')

    def __str__(self):
        return self.title

