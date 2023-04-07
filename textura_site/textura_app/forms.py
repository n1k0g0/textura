from django import forms
from .models import  UploadedText, CorpusEntityData, FiltersModel
 


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
    

class FiltersForm(forms.ModelForm):
    class Meta:
        model = FiltersModel
        fields = [
            "author", 
            "category", 
            "time_period",
            "created",
            "genre_fi",
            "texttype",
            "topic",
            "chronotop",
            "style",
            "subcorpus"
            ]
        labels = {
            "author": "Автор",
            "category": "Категория",
            "time_period": "Век создания",
            "created": "Год создания",
            "genre_fi": "Жанр",
            "texttype": "Тип текста",
            "topic": "Тема",
            "chronotop": "Создан в",
            "style": "Стиль текста",
            "subcorpus": "Подкорпус" 
        }
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': 'А. С. Пушкин'}),
            'category': forms.TextInput(attrs={'placeholder': 'Письма'}),
            'time_period': forms.TextInput(attrs={'placeholder': 'xix'}),
            'created': forms.TextInput(attrs={'placeholder': '1836'}),
            'genre_fi': forms.TextInput(attrs={'placeholder': 'историческая проза'}),
            'texttype': forms.TextInput(attrs={'placeholder': 'монография'}),
            'topic': forms.TextInput(attrs={'placeholder': 'история'}),
            'chronotop': forms.TextInput(attrs={'placeholder': 'Россия: XVIII век'}),
            'style': forms.TextInput(attrs={'placeholder': 'официальный'}),
            'subcorpus': forms.TextInput(attrs={'placeholder': 'ПК письменных текстов'}),
        }
    def clean(self):
        super(FiltersForm, self).clean()
        return self.cleaned_data
        
    
        