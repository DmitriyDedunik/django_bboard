from os import access
from re import template
from django.shortcuts import render
from django.http import HttpResponse
from .models import Bb
from django.views.generic.edit import CreateView
from .forms import BbForm

# def index(request):
#     context = 'Доска объявлений\n\n'
#     for bb in Bb.objects.all():
#         context += f'{bb.title} - {bb.price}\n{bb.content}\n{bb.published}\n\n'

#     return HttpResponse(context, content_type='text\plain; charset=cp1251')

def index(request):
    template = 'bboard/index.html'
    bbs = Bb.objects.all()
    context = {'bbs': bbs}
    return render(request, template, context)

class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    saccess_url = '/bboard/'

def BbCreateView_new(request):

    if request.method == "POST":      
        
        form = BbForm(request.POST)
        form.save()

        # bb = Bb.objects.create()
        # bb.title = request.POST.title
        # bb.content = request.POST.content
        # bb.price = request.POST.price
        # bb.rubric = request.POST.rubric
        # bb.save()

        template = 'bboard/index.html'
        bbs = Bb.objects.all()
        context = {'bbs': bbs}
        return render(request, template, context)

    else:
        template = 'bboard/create_new.html'
        form = BbForm()
        context = {'form': form}
        return render(request, template, context)   

    



