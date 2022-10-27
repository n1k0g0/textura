from django import forms
from .models import CorporaEntityData, UploadedText
 
 
# creating a form
class CorporaEntityForm(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = CorporaEntityData
 
        # specify fields to be used
        fields = [
            "title",
            "time_period",
            "category"
        ]

#### TODO: добавить прочие поля типологии
class UploadTextForm(forms.ModelForm):
    class Meta:
        model = UploadedText
        fields = ['title', 'file']
        labels = {
        "title": "Название",
        "file": "Файл"
        }