from django import forms
from .models import CorporaEntityData, UploadedText, CorpusEntityData
from django.core.exceptions import ValidationError
 
 
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

class CorpusEntityForm(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = CorpusEntityData
 
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
        fields = ['title', 'file', 'author', 'category', 'time_period']
        labels = {
        "title": "Название",
        "file": "Файл",
        "author": "Автор",
        "category": "Категория",
        "time_period": "Век создания"
        }
    def clean(self):
 
        
        super(UploadTextForm, self).clean()
        filename = self.cleaned_data.get('file')
        # print(filename)
        if filename:
            # print(filename.name.split('.')[-1])
            if filename.name.split('.')[-1] not in ['txt', 'TXT']:
                self._errors['file'] = self.error_class([
                'Необходимо расширение .txt'])

        #    raise ValidationError("File is not .txt")
        
        # return any errors if found
        return self.cleaned_data
        
    
        