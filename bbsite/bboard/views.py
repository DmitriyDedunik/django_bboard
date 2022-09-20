"""Describe project views."""
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Case, Count, Q, When
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpRequest, HttpResponse
from .forms import BbForm, ChatForm, CityForm, RegistrationUserForm, RubricForm
from .models import Bb, Chat, Rubric
import requests
import json
import urllib.parse

logger = logging.getLogger(__name__)

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
    logger.info('Запуск страницы рубрик') #логирование
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
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        logger.info('Создание рубрики: ' + request.POST['name']) #логирование
        return super().post(request, *args, **kwargs)
    

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
    form = AuthenticationForm()
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:

        params = {
            'client_id': '707920910456-p8h5a6o68t5kdbq3a28vii9oh7i18hov.apps.googleusercontent.com',
            'redirect_uri': 'http://localhost:8000/google_response/',
            'response_type': 'code',
            'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
            'state': 123,
            'prompt': 'select_account',
        }

        safe_string = 'https://accounts.google.com/o/oauth2/auth?'
        safe_string += urllib.parse.urlencode(params)

        return render(request, self.template_name, {'google_link': safe_string, 'form': self.form})
    

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


def yandex_response(request):
    code = request.GET['code']
    response_token = requests.post(
        'https://oauth.yandex.ru/token', {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': '62d3ee47742b47979d64e1208e58fed0',
            'client_secret': '4f64ebc5e63b448796253d2ebfba1b45',
            }
    )

    detail_response_token = json.loads(response_token.content.decode('utf8').replace("'", '"'))
    token = detail_response_token['access_token']
    
    headers = {'Authorization': 'OAuth ' +  token}
    response_user = requests.get('https://login.yandex.ru/info?format=json', headers=headers)
    detail_response_user = json.loads(response_user.content.decode('utf8').replace("'", '"'))
    email = detail_response_user['default_email']
    user_name = detail_response_user['login']
    password = detail_response_user['id']

    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        user = User.objects.create_user(user_name, email, password)
        
    login(request, user)

    return redirect(reverse('bboard:index'))


def google_response(request):
    code = request.GET['code']
    response_token = requests.post(
        'https://accounts.google.com/o/oauth2/token', {
            'client_id': '707920910456-p8h5a6o68t5kdbq3a28vii9oh7i18hov.apps.googleusercontent.com',
            'client_secret': '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',
            'redirect_uri': 'http://localhost:8000/google_response/',
            'grant_type': 'authorization_code',
            'code': code,
            }
    )

    detail_response_token = json.loads(response_token.content.decode('utf8').replace("'", '"'))
    token = detail_response_token['access_token']
    id_token = detail_response_token['id_token']

    params = {
        'access_token': token,
        'id_token': id_token,
        'token_type': 'Bearer',
        'expires_in': 3599,
    }

    response_user = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?' + urllib.parse.urlencode(params))
    detail_response_user = json.loads(response_user.content.decode('utf8').replace("'", '"'))
    email = detail_response_user['email']
    user_name = detail_response_user['name']
    password = detail_response_user['id']

    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        user = User.objects.create_user(user_name, email, password)
        
    login(request, user)

    return redirect(reverse('bboard:index'))
