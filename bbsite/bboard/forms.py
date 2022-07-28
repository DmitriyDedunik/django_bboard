"""Describe project forms."""
from django.contrib.auth.forms import UserModel, UserCreationForm

from bboard.models import Bb, City, Rubric

from django.forms import ModelForm, Textarea, TextInput





class BbForm(ModelForm):
    """Describe form by bb model."""

    class Meta:  # noqa: WPS306
        """Describe form properties."""

        model = Bb
        fields = ('title', 'price', 'content', 'rubric', 'city', 'image')

        widgets = {
            'title': TextInput(attrs={
                'PlaceHolder': 'Наименование',
            }),
            'content': Textarea(attrs={
                'PlaceHolder': 'Описание',
            }),
        }


class RubricForm(ModelForm):
    """Describe form by rubric model."""

    class Meta(object):
        """Describe form properties."""

        model = Rubric
        fields = ('name',)


class CityForm(ModelForm):
    """Describe form by city model."""

    class Meta(object):
        """Describe form properties."""

        model = City
        fields = ('name',)


class RegistrationUserForm(UserCreationForm):
    """Describe form by city model."""

    class Meta(object):
        """Describe form properties."""

        model = UserModel
        fields = ('username', 'password1', 'password2')