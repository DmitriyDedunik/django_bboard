from django.forms import ModelForm, TextInput, Textarea, NumberInput
from .models import Bb, Rubric, City

class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'price', 'content', 'rubric', 'city', 'image')

        widgets = {
            'title': TextInput(attrs={
                'PlaceHolder': 'Наименование'
            }),           
            'content': Textarea(attrs={
                'PlaceHolder': 'Описание'
            })              
            }


class RubricForm(ModelForm):
    class Meta:
        model = Rubric
        fields = ('name',)


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ('name',)