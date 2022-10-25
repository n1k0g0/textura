from django import forms
from .models import TextData, Text
 
 
# creating a form
class TextForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = TextData
 
        # specify fields to be used
        fields = [
            "title",
            "time_period",
            "text_type"
        ]

class AddTextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ('title', 'author', 'category', 'time_period', 'file', 'avg_sentence_length')