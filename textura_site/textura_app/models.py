from django.db import models

# Create your models here.

from django.db import models
  
# declare a new model with a name 
class TextData(models.Model):
 
    # fields of the model
    title = models.CharField(max_length = 200)
    time_period = models.CharField(max_length = 50)
    text_type = models.TextField()
    avg_sentence_length = models.IntegerField() 

    class Meta:
        app_label = 'textura_app'
    # renames the instances of the model
    # with their title names
    def __str__(self):
        return self.title


class Text(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    time_period = models.CharField(max_length = 50)
    category = models.CharField(max_length=50)
    file = models.FileField(upload_to='texts/')
    avg_sentence_length = models.IntegerField() 

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(Text, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title