from django.shortcuts import render, redirect, get_object_or_404
from .metrics import PreprocessedText
from django.http import HttpResponse

import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.graph_objs import Box, Scatter

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

def prepare_charts():
    corpus = CorpusEntityData.objects.all()
    plot_div = dict()

    asl = [entry.avg_sentence_length for entry in corpus if entry.avg_sentence_length is not None]
    awl = [entry.avg_word_length for entry in corpus if entry.avg_word_length is not None]
    asw = [entry.avg_syl_per_word for entry in corpus if entry.avg_syl_per_word is not None]

    plot_div['asl'] = plot([Box(y=asl,
                    opacity=0.8, 
                    marker_color='blue'
                    )],
                    output_type='div'
                    )
    plot_div['awl'] = plot([Box(y=awl,
                    opacity=0.8, 
                    marker_color='blue'
                    )],
                    output_type='div')
    plot_div['asw'] = plot([Box(y=asw,
                    opacity=0.8, 
                    marker_color='blue',
                    )],
                    output_type='div')
    

    ttr = [entry.type_token_ratio for entry in corpus if entry.type_token_ratio is not None]
    ld = [entry.lexical_density for entry in corpus if entry.lexical_density is not None]

    plot_div['ttr'] = plot([Box(y=ttr,
                    opacity=0.8, 
                    marker_color='blue'
                    )],
                    output_type='div')
    plot_div['ld'] = plot([Box(y=ld,
                    opacity=0.8, 
                    marker_color='blue'
                    )],
                    output_type='div')
    

    hwq = [entry.hard_words_quantity for entry in corpus if entry.hard_words_quantity is not None]
    fres = [entry.fres for entry in corpus if entry.fres is not None]
    gunning_fog = [entry.gunning_fog for entry in corpus if entry.gunning_fog is not None]
    ari = [entry.ari for entry in corpus if entry.ari is not None]
    smog = [entry.smog for entry in corpus if entry.smog is not None]
    cli = [entry.cli for entry in corpus if entry.cli is not None]
    
    plot_div['hwq'] = plot([Box(y=hwq,
                    opacity=0.8, 
                    marker_color='blue'
                    )],
                    output_type='div')
    plot_div['fres'] = plot([Box(y=fres,
                    opacity=0.8, 
                    marker_color='blue'
                    )],
                    output_type='div')
    plot_div['gunning_fog'] = plot([Box(y=gunning_fog,
                    opacity=0.8, 
                    marker_color='blue'
                    )],
                    output_type='div')
    plot_div['ari'] = plot([Box(y=ari,
                    opacity=0.8, 
                    marker_color='blue'
                    )],
                    output_type='div')
    plot_div['smog'] = plot([Box(y=smog,
                    opacity=0.8, 
                    marker_color='blue'
                    )],
                    output_type='div')
    plot_div['cli'] = plot([Box(y=cli,
                    opacity=0.8, 
                    marker_color='blue'
                    )],
                    output_type='div')
    
    

    return plot_div



def analysis(request):
    texts = UploadedText.objects.all()
    plot_div = prepare_charts()
    for text in texts:
        print(text.avg_sentence_length)
        if None in [
            text.avg_sentence_length,
            text.type_token_ratio,
            text.hard_words_quantity,
            text.blanchefort_positive
        ]:
            process_text(text)
            plot_div = prepare_charts()

            
    return render(request, 'textura_app/analysis.html', {'texts': texts, 'plot_div': plot_div})





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