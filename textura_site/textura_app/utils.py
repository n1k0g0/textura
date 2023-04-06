from .models import CorpusEntityData

import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.graph_objs import Box

import numpy as np

TEXT_MODEL_PLOT_DICT = {
                "avg_sentence_length": "Ср. длина предложений",
                "avg_word_length": "Ср. длина слов",
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
            # print(key)

            list_of_values_for_column = [float(entry[key]) for entry in corpus if entry[key] is not None and entry[key] != '']
            # print(list_of_values_for_column)
            fig = go.Figure(data = Box(name = TEXT_MODEL_PLOT_DICT[key], y = list_of_values_for_column, opacity=0.7, marker_color='blue', notched=True))

            if len(texts) and key in TEXT_MODEL_PLOT_DICT.keys():
                # print(texts.values()[0])
                current_text_value = texts.values()[0][key]
                text_name = texts.values()[0]['title']
                if len(text_name) > 15:
                    text_name = 'Пользовательский текст'
                formatted_value = "%.2f" % texts.values()[0][key] if texts.values()[0][key] is not None else '-'
                text_name = f'{formatted_value} – ' + text_name
                
                q3, q1 = np.percentile(list_of_values_for_column, [75 ,25])
                iqr = abs(q3 - q1)
                lower_fence, upper_fence = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                #print(lower_fence, q1, q3, upper_fence)
                #print(current_text_value)
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