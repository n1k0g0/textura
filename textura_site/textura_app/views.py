from django.shortcuts import render, redirect, get_object_or_404
 
# relative import of forms
from .models import TextData, Text
from .forms import TextForm, AddTextForm
from django.contrib import messages
 
 
def create_view(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = TextForm(request.POST or None)
    if form.is_valid():
        form.save()
         
    context['form']= form
    return render(request, "textura_app/create_view.html", context)


def home(request):
    texts = TextData.objects.all()[0:1000]
    return render(request, 'textura_app/home.html', {'texts': texts})


def add_text(request):
    if request.method == 'POST':
        form = AddTextForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            messages.success(request, "text added successfully")
            return redirect('home')
    else:
        form = AddTextForm()
    return render(request, 'textura_app/add_text.html', {'form': form})


def delete_text(request, pk):
    if request.method == 'POST':
        text = get_object_or_404(Text, pk=pk)
        text.delete()
        messages.success(request, "text deleted successfully")
        return redirect('home')
    else:
        return redirect('home')