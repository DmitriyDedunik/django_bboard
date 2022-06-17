from dataclasses import fields
from msilib.schema import Class
from pyexpat import model
from django.forms import ModelForm
from .models import Bb

class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'price', 'content', 'rubric')