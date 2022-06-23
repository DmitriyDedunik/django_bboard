from dataclasses import fields
from msilib.schema import Class
from pyexpat import model
from unicodedata import name
from django.forms import ModelForm
from .models import Bb, Rubric

class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'price', 'content', 'rubric')

class RubricForm(ModelForm):
    class Meta:
        model = Rubric
        fields = ('name',)