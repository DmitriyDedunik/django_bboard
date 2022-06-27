from django.forms import ModelForm, TextInput, Textarea
from .models import Bb, Rubric

class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'price', 'content', 'rubric')

        widgets = {
            'title': TextInput(attrs={
                'PlaceHolder': 'Наименование'
            }),
            'content': Textarea(attrs={
                'PlaceHolder': 'Описание'
            }),
            'rubric': TextInput(attrs={
                'PlaceHolder': 'Рубрика'
            }),              
            }

class RubricForm(ModelForm):
    class Meta:
        model = Rubric
        fields = ('name',)