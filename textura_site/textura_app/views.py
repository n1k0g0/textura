from django.shortcuts import render, redirect, get_object_or_404
from .metrics import PreprocessedText

from .models import CorporaEntityData, UploadedText
from .forms import CorporaEntityForm, UploadTextForm

 
def add_corpora_entity(request):
    context = {}
    form = CorporaEntityForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form']= form
    return render(request, "textura_app/add_corpora_entity.html", context)


def show_corpora(request):
    texts = CorporaEntityData.objects.all()[0:1000]
    return render(request, 'textura_app/show_corpora.html', {'texts': texts})


def analysis(request):
    texts = UploadedText.objects.all()
    for text in texts:
        preprocessed_text = PreprocessedText(text.file.name)
        
        if text.avg_sentence_length == None:
                text.avg_sentence_length = preprocessed_text.asl
        if text.avg_sentence_length_stdev == None:
                text.avg_sentence_length_stdev = preprocessed_text.asl_stdev
        if text.avg_sentence_length_rank == None:
                text.avg_sentence_length_rank = preprocessed_text.asl_rank
        if text.max_sentence_length == None:
                text.max_sentence_length = preprocessed_text.msl

        if text.avg_word_length == None:
                text.avg_word_length = preprocessed_text.awl
        if text.avg_word_length_stdev == None:
                text.avg_word_length_stdev = preprocessed_text.awl_stdev
        if text.max_word_length == None:
                text.max_word_length = preprocessed_text.mwl
        
    return render(request, 'textura_app/analysis.html', {'texts': texts})


def upload_text(request):
    if request.method == 'POST':
        texts = UploadedText.objects.all()
        for text in texts:
            text.delete()

        form = UploadTextForm(request.POST, request.FILES)
        
        if form.is_valid():

            form_mutable = form.save(commit=False)
            print(form_mutable.file.path)
            if form_mutable.title == None:
                form_mutable.title = form_mutable.file.name
            if form_mutable.time_period == None:
                form_mutable.time_period = '-'
            if form_mutable.author == None:
                form_mutable.author = '-'
            if form_mutable.category == None:
                form_mutable.category = '-'
            
            form_mutable.save()
            

            return redirect('analysis')
        else:

            return render(request, 'textura_app/upload_text.html', {'form': form})
    form = UploadTextForm(None)  
    return render(request, 'textura_app/upload_text.html', {'form':form})


def delete_text(request, pk):
    if request.method == 'POST':
        text = get_object_or_404(UploadedText, pk=pk)
        text.delete()
        return redirect('upload_text')
    else:
        return redirect('analysis')