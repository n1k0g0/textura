from django.shortcuts import render, redirect, get_object_or_404
from .metrics import PreprocessedText
from .utils import prepare_charts
from django.http import HttpResponse, HttpResponseRedirect

from .models import  UploadedText, CorpusEntityData, FiltersModel
from .forms import  UploadTextForm, CorpusEntityForm, FiltersForm



 
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




def process_text(text):
    preprocessed_text = PreprocessedText(text.file.name)
    if text.avg_sentence_length is None:
        preprocessed_text.load_basics()
    if text.type_token_ratio is None:
        preprocessed_text.load_vocab()
    if text.hard_words_quantity is None:
        preprocessed_text.load_complexity()
    if text.blanchefort_positive is None:
        preprocessed_text.load_sentiment()
        


    text.avg_sentence_length = preprocessed_text.asl
    text.avg_sentence_length_stdev = preprocessed_text.asl_stdev
    text.avg_sentence_length_median = preprocessed_text.asl_med
    text.avg_sentence_length_iqr = preprocessed_text.asl_iqr
    text.max_sentence_length = preprocessed_text.msl
    
    text.avg_word_length = preprocessed_text.awl
    text.avg_word_length_median = preprocessed_text.awl_med
    text.avg_word_length_iqr = preprocessed_text.awl_iqr
    text.avg_word_length_stdev = preprocessed_text.awl_stdev
    text.max_word_length = preprocessed_text.mwl
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
    text.save()

    



def analysis_graphs(request):
    texts = UploadedText.objects.all()
    filters_values_list = FiltersModel.objects.values()
    # plot_div = prepare_charts(filters_values_list, texts)
    for text in texts:
        # print(text.avg_sentence_length)
        if None in [
            text.avg_sentence_length,
            text.type_token_ratio,
            text.hard_words_quantity,
            text.blanchefort_positive
        ]:
            process_text(text)
    plot_div = prepare_charts(filters_values_list, texts)

            
    return render(request, 'textura_app/analysis.html', {'texts': texts, 'plot_div': plot_div})



def analysis(request):
    texts = UploadedText.objects.all()
    for text in texts:
        if None in [
            text.avg_sentence_length,
            text.type_token_ratio,
            text.hard_words_quantity,
            text.blanchefort_positive
        ]:
            process_text(text)

            
    return render(request, 'textura_app/analysis.html', {'texts': texts})





def upload_text(request):
    if request.method == 'POST':
        texts = UploadedText.objects.all()
        for text in texts:
            text.delete()

        form = UploadTextForm(request.POST, request.FILES)
        
        if form.is_valid():
            form_mutable = form.save(commit=False)
            # print(form_mutable.file.path)
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
    



def update_text(request, pk):
    context ={}
    obj = get_object_or_404(UploadedText, id = pk)
    form = UploadTextForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.save()
        return redirect('analysis') 
    context["form"] = form

    return render(request, "textura_app/update_text.html", context)






def update_filters(request):
    if request.method == 'POST':
        filters = FiltersModel.objects.all()
        for filter in filters:
            filter.delete()

        form = FiltersForm(request.POST, request.FILES)
        
        if form.is_valid():
            form_mutable = form.save(commit=False)
            if form_mutable.time_period == None:
                form_mutable.time_period = '-'
            if form_mutable.author == None:
                form_mutable.author = '-'
            if form_mutable.category == None:
                form_mutable.category = '-'
            
            form_mutable.save()
            

            return redirect('analysis')
        else:

            return render(request, 'textura_app/update_filters.html', {'form': form})
    form = FiltersForm(None)  
    return render(request, 'textura_app/update_filters.html', {'form':form})