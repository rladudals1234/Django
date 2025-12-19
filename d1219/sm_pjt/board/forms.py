from django import forms
from .models import Board

from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['btitle', 'bcontent']
        widgets = {
            'bcontent': SummernoteWidget(),
        }