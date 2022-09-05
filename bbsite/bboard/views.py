"""Describe project views."""
from email.policy import default
from itertools import count

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Case, Count, Q, Value, When
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import BbForm, ChatForm, CityForm, RegistrationUserForm, RubricForm
from .models import Bb, Chat, Rubric

ITEMS_PER_PAGE = 2

def index(request):
    
    template = 'bboard/index.html'
    bbs = Bb.objects.all()
    paginator = Paginator(bbs, ITEMS_PER_PAGE)
    
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    rubrics = Rubric.objects.all()
    context = {'bbs': page.object_list, 'rubrics': rubrics, 'page': page}
    
    return render(request, template, context)


def rubrics(request):
    template = 'bboard/rubrics.html'
    rubrics = Rubric.objects.all()
    context = {'rubrics': rubrics}
    return render(request, template, context)    


class LRMixin(LoginRequiredMixin):
    login_url = '/login/'


class CityCreateView(LoginRequiredMixin, CreateView):
    template_name = 'bboard/create_city.html'
    form_class = CityForm
    success_url = reverse_lazy('bboard:index')


class BbDetailView(DetailView):
    model = Bb


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NewUpdate(LRMixin, UpdateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    model = Bb

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('bboard:detail', kwargs={'pk': self.kwargs['pk']})


class BbDeleteView(LRMixin, DeleteView):
    model = Bb
    success_url = reverse_lazy('bboard:index')
        

class RubricCreate(LRMixin, CreateView):
    template_name = 'bboard/create_rubric.html'
    form_class = RubricForm
    success_url = reverse_lazy('bboard:index')
    

@login_required(login_url='/login/')
def BbCreateView_new(request):

    if request.method == "POST":      
        
        form = BbForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bboard:index')
        else:
            error = 'Форма была не верной'
            template = 'bboard/create_new.html'
            context = {'form': form, 'error': error}
            return render(request, template, context)

    else:
        template = 'bboard/create_new.html'
        form = BbForm()
        rubrics = Rubric.objects.all()
        context = {'form': form, 'rubrics': rubrics}
        return render(request, template, context)   


def by_rubric(request, rubric_id):
    template = 'bboard/index.html'
    rubric = Rubric.objects.get(pk=rubric_id)
    bbs = rubric.bbs.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubric': rubric, 'rubrics': rubrics}
    return render(request, template, context)


class Registration(CreateView):
    form_class = RegistrationUserForm
    success_url = reverse_lazy('login')
    template_name = 'registration.html'


class UserLogin(LoginView):
    template_name = 'registration/login.html'
    

def my_bb(request):
    template = 'bboard/index.html'
    bbs = Bb.objects.filter(user_id=request.user.id)
    context = {'bbs': bbs, 'rubrics': {}}
    return render(request, template, context)


def send_message(request, bb_id, user_id):
    
    bb = get_object_or_404(Bb, pk=bb_id)
    user_to = get_object_or_404(User, pk=user_id)
    chat = Chat.objects.filter(
        Q(
            Q(Q(user_from=request.user)&Q(user_to=user_to))|
            Q(Q(user_from=user_to)&Q(user_to=request.user))
        )&
        Q(bb=bb)
    )
    
    if request.method == "POST":      
        
        form = ChatForm(request.POST)
        if form.is_valid():
            form_chat = form.save(commit=False)
            form_chat.user_from = request.user
            form_chat.user_to = user_to
            form_chat.bb = bb
            form_chat.save()

            return redirect(reverse(
                'bboard:send_message', 
                kwargs={'bb_id': bb_id, 'user_id': user_id}
            ))
        else:
            error = 'Форма была не верной'
            template = 'bboard/chat.html'
            context = {'form': form, 'error': error}
            return render(request, template, context)

    else:
        template = 'bboard/chat.html'
        form = ChatForm()
        context = {'form': form, 'bb': bb, 'chat': chat}
        return render(request, template, context)

def chats(request):
        
        template = 'bboard/chats.html'
        chats = Chat.objects.filter(
            Q(
                Q(user_from=request.user)|
                Q(user_to=request.user)
            )
        )

        chats = chats.annotate(
            chat_user = Case(
                When(Q(user_from=request.user), then='user_to'),
                default='user_from'
            ),
            chat_username = Case(
                When(Q(user_from=request.user), then='user_to__username'),
                default='user_from__username'
            )
        )

        chats = chats.values('bb', 'chat_user', 'bb__title', 'chat_username')

        chats = chats.annotate(count=Count('chat_user', distinct=True))

        context = {'chats': chats}
        
        return render(request, template, context)
