from django.shortcuts import redirect, render
from django.urls import reverse_lazy
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
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, template, context)

def rubrics(request):
    template = 'bboard/rubrics.html'
    rubrics = Rubric.objects.all()
    context = {'rubrics': rubrics}
    return render(request, template, context)    


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('bbsite_app:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class RubricCreate(CreateView):
    template_name = 'bboard/create_rubric.html'
    form_class = RubricForm
    success_url = reverse_lazy('bbsite_app:index')
    

def BbCreateView_new(request):

    if request.method == "POST":      
        
        form = BbForm(request.POST)
        if form.is_valid():
            form.save()

        # bb = Bb.objects.create()
        # bb.title = request.POST['title']
        # bb.content = request.POST['content']
        # bb.price = request.POST['price']
        # bb.rubric = Rubric.objects.get(pk=request.POST['rubric'])
        # bb.save()

        return redirect('bbsite_app:index')
        # template = 'bboard/index.html'
        # bbs = Bb.objects.all()
        # rubrics = Rubric.objects.all()
        # context = {'bbs': bbs, 'rubrics': rubrics}
        # return render(request, template, context)

    else:
        template = 'bboard/create_new.html'
        form = BbForm()
        rubrics = Rubric.objects.all()
        context = {'form': form, 'rubrics': rubrics}
        return render(request, template, context)   

def by_rubric(request, rubric_id):
    template = 'bboard/index.html'
    rubric = Rubric.objects.get(pk=rubric_id)
    bbs = Bb.objects.filter(rubric = rubric)
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubric': rubric, 'rubrics': rubrics}
    return render(request, template, context)

