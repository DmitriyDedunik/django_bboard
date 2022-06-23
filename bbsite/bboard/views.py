from os import access
from re import template
from django.shortcuts import render
from django.http import HttpResponse
from .models import Bb, Rubric
from django.views.generic.edit import CreateView
from .forms import BbForm, RubricForm

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

def rubrics(request):
    template = 'bboard/rubrics.html'
    rubrics = Rubric.objects.all()
    context = {'rubrics': rubrics}
    return render(request, template, context)    

class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = '/bboard/'

class RubricCreate(CreateView):
    template_name = 'bboard/create_rubric.html'
    form_class = RubricForm
    success_url = '/bboard/'

def BbCreateView_new(request):

    if request.method == "POST":      
        
        # form = BbForm(request.POST)
        # form.save()

        bb = Bb.objects.create()
        bb.title = request.POST['title']
        bb.content = request.POST['content']
        bb.price = request.POST['price']
        bb.rubric = Rubric.objects.get(pk=request.POST['rubric'])
        bb.save()

        template = 'bboard/index.html'
        bbs = Bb.objects.all()
        context = {'bbs': bbs}
        return render(request, template, context)

    else:
        template = 'bboard/create_new.html'
        form = BbForm()
        context = {'form': form}
        return render(request, template, context)   

def by_rubric(request, rubric_id):
    template = 'bboard/by_rubric.html'
    rubric = Rubric.objects.get(pk=rubric_id)
    bbs = Bb.objects.filter(rubric = rubric)
    context = {'bbs': bbs, 'rubric': rubric}
    return render(request, template, context)

