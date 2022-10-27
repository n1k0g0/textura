from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

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
    return render(request, 'textura_app/analysis.html', {'texts': texts})


def upload_text(request):
    if request.method == 'POST':
        form = UploadTextForm(request.POST, request.FILES)
        print('uploaded')
        if form.is_valid:
            form.save()
            messages.success(request, "text added successfully")
            return redirect('analysis')
    else:
        form = UploadTextForm()
    return render(request, 'textura_app/upload_text.html', {'form': form})


def delete_text(request, pk):
    if request.method == 'POST':
        text = get_object_or_404(UploadedText, pk=pk)
        text.delete()
        messages.success(request, "text deleted successfully")
        return redirect('analysis')
    else:
        return redirect('analysis')