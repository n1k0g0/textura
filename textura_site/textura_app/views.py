from django.shortcuts import render, redirect, get_object_or_404
from .metrics import PreprocessedText
from django.http import HttpResponse, HttpResponseRedirect

import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.graph_objs import Box, Scatter

import numpy as np


from .models import CorporaEntityData, UploadedText, CorpusEntityData, FiltersModel
from .forms import CorporaEntityForm, UploadTextForm, CorpusEntityForm, FiltersForm

TEXT_MODEL_PLOT_DICT = {
                "avg_sentence_length": "Ср. длина предложения",
                "avg_word_length": "Ср. длина слова",
                "avg_syl_per_word": "Ср. кол-во слогов в словах",
                "type_token_ratio": "Коэф. лексического разнообразия",
                "lexical_density": "Коэф. лексической плотности",
                "hard_words_quantity": "Кол-во многосложных слов",
                "fres": "FRES",
                "gunning_fog": "Gunning Fog",
                "ari": "Индекс удобочитаемости",
                "smog": "SMOG",
                "cli": "CLI"
}

 
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
    text.save()


# def process(request):
#     if request.method == 'GET':
#            print(request)
#            text_id = request.GET['text_id']
#            text = get_object_or_404(UploadedText, pk=text_id)
#            # likedpost = Post.objects.get(pk=text_id) #getting the liked posts
#            process_text(text)
#            #m = Like(post=likedpost) # Creating Like Object
#            #m.save()  # saving it to store in database
#            return HttpResponse("Success!") # Sending an success response
#     else:
#            return HttpResponse("Request method is not a GET")

def prepare_charts(filters_list, texts):
    print(filters_list)
    corpus_objects = CorpusEntityData.objects.all()
    for filter in filters_list:
        if filter['author'] != '-':
            corpus_objects = corpus_objects.filter(author=filter['author'])
        if filter['time_period'] != '-':
            corpus_objects = corpus_objects.filter(time_period=filter['time_period'])
        if filter['category'] != '-':
            corpus_objects = corpus_objects.filter(category=filter['category'])
        
        
    corpus = corpus_objects.values()
    plot_div = dict()

    if len(corpus):
        # print(corpus[0].keys())
        for key in TEXT_MODEL_PLOT_DICT.keys():

            list_of_values_for_column = [entry[key] for entry in corpus if entry[key] is not None]
            fig = go.Figure(data = Box(name = TEXT_MODEL_PLOT_DICT[key], y = list_of_values_for_column, opacity=0.7, marker_color='blue'))

            if len(texts) and key in TEXT_MODEL_PLOT_DICT.keys():
                # print(texts.values()[0].keys())
                current_text_value = texts.values()[0][key]
                text_name = texts.values()[0]['title']
                if len(text_name) > 15:
                    text_name = 'Пользовательский текст'
                formatted_value = "%.2f" % texts.values()[0][key]
                text_name = f'{formatted_value} – ' + text_name
                
                q3, q1 = np.percentile(list_of_values_for_column, [75 ,25])
                iqr = abs(q3 - q1)
                lower_fence, upper_fence = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                print(lower_fence, q1, q3, upper_fence)
                if current_text_value > q1 and current_text_value < q3:
                    fig.update_traces(marker_color='lightseagreen')
                    fig.update_layout(title_text=f'{TEXT_MODEL_PLOT_DICT[key]} в норме!')
                elif current_text_value > upper_fence or current_text_value < lower_fence:
                    fig.update_traces(marker_color='indianred')
                    fig.update_layout(title_text='Сильное отклонение от нормы!')
                else:
                    fig.update_layout(title_text=f'{TEXT_MODEL_PLOT_DICT[key]} близко к норме!')

                fig.update_layout(
                                # yaxis_title = 'Y_Axis',
                                margin={'b':30,'l':0,'r':0,'t':30}
                                )
                fig.add_hline(
                    y=current_text_value,
                    annotation_text=text_name,
                    annotation_position='top left'
                    )
            
            #Turn graph object into local plotly graph
            plot_div[key] = plot({'data': fig}, output_type='div')

    return plot_div

    



def analysis(request):
    texts = UploadedText.objects.all()
    filters_values_list = FiltersModel.objects.values()
    plot_div = prepare_charts(filters_values_list, texts)
    for text in texts:
        # print(text.avg_sentence_length)
        if None in [
            text.avg_sentence_length,
            text.type_token_ratio,
            text.hard_words_quantity,
            text.blanchefort_positive
        ]:
            process_text(text)
            # plot_div = prepare_charts(filters_values_list, texts)

            
    return render(request, 'textura_app/analysis.html', {'texts': texts, 'plot_div': plot_div})





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
            # print(form_mutable.file.path)
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