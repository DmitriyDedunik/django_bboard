from distutils.log import error
from xml.parsers.expat import model
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Bb, Rubric
from django.views.generic.edit import CreateView, UpdateView
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


class New_update(UpdateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('bbsite_app:index')
    model = Bb
    
    pk_new_id = 'new_id'

    def get_object(self, new_id=None):
        return self.model.objects.get(pk=self.kwargs.get(self.pk_new_id))
        

class RubricCreate(CreateView):
    template_name = 'bboard/create_rubric.html'
    form_class = RubricForm
    success_url = reverse_lazy('bbsite_app:index')
    

def BbCreateView_new(request):

    if request.method == "POST":      
        
        form = BbForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bbsite_app:index')
        else:
            error = 'Форма была не верной'
            template = 'bboard/create_new.html'
            context = {'form': form, 'error': error}
            return render(request, template, context)

        # bb = Bb.objects.create()
        # bb.title = request.POST['title']
        # bb.content = request.POST['content']
        # bb.price = request.POST['price']
        # bb.rubric = Rubric.objects.get(pk=request.POST['rubric'])
        # bb.save()
       
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

# def home(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#         form.set_user_id(request.user.id)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/seller')
#         else:
#             print('errors')
#             print(form.errors)
#     else:
#         try:
#             profile = Profile.objects.get(user_id=request.user.id)
#             form = ProfileForm(instance=profile)
#         except Profile.DoesNotExist:
#             form = ProfileForm()
#     return render(request, "seller/home.html", {'form': form})
