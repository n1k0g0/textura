from django.core.validators import FileExtensionValidator

from django.db import models
import magic  

# declare a new model with a name 
class CorporaEntityData(models.Model):
 
    title = models.CharField(max_length = 200)
    time_period = models.CharField(max_length = 50)
    category = models.TextField()
    avg_sentence_length = models.FloatField(default=None, blank=True, null=True) 
    avg_word_length = models.FloatField(default=None, blank=True, null=True) 

    class Meta:
        app_label = 'textura_app'
    # renames the instances of the model
    # with their title names
    def __str__(self):
        return self.title


class UploadedText(models.Model):
    file = models.FileField(upload_to='texts/', validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    title = models.CharField(max_length=100, default=None, blank=True, null=True)
    author = models.CharField(max_length=100, default=None, blank=True, null=True)
    time_period = models.CharField(max_length = 50, default=None, blank=True, null=True)
    category = models.CharField(max_length=50, default=None, blank=True, null=True)
    avg_sentence_length = models.FloatField(default=None, blank=True, null=True) 
    avg_sentence_length_stdev = models.FloatField(default=None, blank=True, null=True) 
    avg_sentence_length_rank = models.FloatField(default=None, blank=True, null=True) 
    max_sentence_length = models.FloatField(default=None, blank=True, null=True) 
    
    avg_word_length = models.FloatField(default=None, blank=True, null=True) 
    avg_word_length_stdev = models.FloatField(default=None, blank=True, null=True) 
    avg_word_length_rank = models.FloatField(default=None, blank=True, null=True) 
    max_word_length = models.FloatField(default=None, blank=True, null=True) 

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(UploadedText, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title


