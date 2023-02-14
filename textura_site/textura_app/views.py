from django.shortcuts import render, redirect, get_object_or_404
from .metrics import PreprocessedText

from .models import CorporaEntityData, UploadedText, CorpusEntityData
from .forms import CorporaEntityForm, UploadTextForm, CorpusEntityForm

 
def add_corpora_entity(request):
    context = {}
    form = CorpusEntityForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form']= form
    return render(request, "textura_app/add_corpora_entity.html", context)


def show_corpora(request):
    texts = CorpusEntityData.objects.all()[0:1000]
    return render(request, 'textura_app/show_corpora.html', {'texts': texts})


def analysis(request):
    texts = UploadedText.objects.all()
    for text in texts:
        preprocessed_text = PreprocessedText(text.file.name)
        preprocessed_text.load_basics()
        preprocessed_text.load_vocab()
        preprocessed_text.load_complexity()
        preprocessed_text.load_sentiment()
        
        text.avg_sentence_length = preprocessed_text.asl
        text.avg_sentence_length_stdev = preprocessed_text.asl_stdev
        text.avg_sentence_length_rank = preprocessed_text.asl_rank
        text.max_sentence_length = preprocessed_text.msl
        text.sentence_count = preprocessed_text.s_count 

        text.avg_word_length = preprocessed_text.awl
        text.avg_word_length_rank = preprocessed_text.awl_rank
        text.avg_word_length_stdev = preprocessed_text.awl_stdev
        text.max_word_length = preprocessed_text.mwl
        text.word_count = preprocessed_text.w_count

        text.avg_syl_per_word = preprocessed_text.asw


        text.type_token_ratio = preprocessed_text.ttr
        text.lexical_density = preprocessed_text.lex_den

        text.hard_words_quantity = preprocessed_text.hwq
        text.fres = preprocessed_text.fres
        text.gunning_fog = preprocessed_text.gunning_fog
        text.ari = preprocessed_text.ari
        text.smog = preprocessed_text.smog
        text.cli = preprocessed_text.cli

        text.blanchefort_positive = preprocessed_text.blanchefort_positive
        text.blanchefort_neutral = preprocessed_text.blanchefort_neutral
        text.blanchefort_negative = preprocessed_text.blanchefort_negative
        
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