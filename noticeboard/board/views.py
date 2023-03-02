from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth import logout
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Count

from .forms import EmailSendForm, SignUpForm, AdForm, ResponseAdForm
from .tokens import account_activation_token
from .models import Ad, ResponseAd, AdStatus, ResponseAdStatus
from .filters import AdFilter, AdsFilter


def hello(request):
    return render(request, 'hello.html', {'user': request.user})


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html', {'user': request.user})


def send_email(request):
    if request.method == 'POST':
        form = EmailSendForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            header = form.cleaned_data['header']
            text = form.cleaned_data['text']

            print(email, header, text)
    else:
        form = EmailSendForm()
    return render(request, 'email_send.html', {'form': form})


def logout_view(request):
    next_page = request.GET.get('next', '/')
    print(next_page)
    logout(request)
    return redirect(next_page)


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/board/login'

    template_name = 'registration/signup.html'


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                subject, message, to=[user.email]
            )
            try:
                email.send()
            except BaseException :
                print('Ошибка')

            print('Письмо отправлено')
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'registration/account_activation_invalid.html')


class AdCreateView(CreateView):
    form_class = AdForm
    # fields = ['title', 'image', 'category', 'body']
    template_name = 'ad_create.html'
    success_url = reverse_lazy('hello') #Поменять на мои объявления

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.status = AdStatus.ACTIVE
            ad.save()
            return redirect('ad_my_list')
    else:
        form = AdForm()
        form.fields['status'].widget.attrs['readonly'] = True #ToDo не работает, потом разобраться
    return render(request, 'ad_create.html', {'form': form})

@login_required
def ad_my_list(request):
    ads = Ad.objects.filter(author=request.user)
    context = {'ads': []}
    for ad in ads:
        count_responses = ResponseAd.objects.filter(ad=ad).count()
        context['ads'].append({'ad': ad, 'responses_count': count_responses})
    return render(request, 'ad_my_list.html', context)

@method_decorator(login_required, name='dispatch')
class AdMyListView(ListView):
    model = Ad
    template_name = 'ad_my_list.html'
    context_object_name = 'ads'
    paginate_by = 1

    def get_queryset(self):
        queryset = Ad.objects.filter(author=self.request.user)
        self.filterset = AdFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

        # for ad in context['ads']:
        #     ad.count_responses = ResponseAd.objects.filter(ad=ad).count()

        return context


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ad = self.get_object()
        context['ad'] = ad
        # context['request'] = self.request
        responseAd = ResponseAd.objects.filter(ad=ad)
        context['response_ad'] = responseAd

        user = self.request.user
        if user.is_authenticated:
            if ad.author == user:
                resp = ResponseAd.objects.filter(ad=ad)
            else:
                resp = ResponseAd.objects.filter(ad=ad, author=self.request.user)

            context['resp'] = resp

        return context

@method_decorator(login_required, name='dispatch')
class AdUpdateView(UpdateView):
    form_class = AdForm
    model = Ad
    template_name = 'ad_edit.html'
    context_object_name = 'ad'
    success_url = reverse_lazy('ad_my_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ad = self.get_object()

        user = self.request.user
        if user.is_authenticated:
            if ad.author == user:
                resp = ResponseAd.objects.filter(ad=ad)
            else:
                resp = ResponseAd.objects.filter(ad=ad, author=self.request.user)

            context['resp'] = resp

        context['ad'] = ad

        return context


class AdsListView(ListView):
    model = Ad
    template_name = 'ads_list.html'
    context_object_name = 'ads'
    paginate_by = 1

    def get_queryset(self):
        # queryset = Ad.objects.select_related('responses').filter(status=AdStatus.ACTIVE)
        queryset = Ad.objects.filter(status=AdStatus.ACTIVE)
        self.filterset = AdsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['request'] = self.request

        if self.request.user.is_authenticated:
            for ad in context['ads']:
                ad.resp = ResponseAd.objects.filter(ad=ad, author=self.request.user)

        return context

@login_required
def add_response(request, ad_id):
    next_url = request.GET.get('next')

    ad = Ad.objects.get(pk=ad_id)
    if request.method == 'POST':
        form = ResponseAdForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ad = ad
            response.author = request.user
            response.save()

            subject = 'Оповещение'
            message = render_to_string('mails/response.html', {
                'ad': ad,
                'resp': response,
            })
            email = EmailMessage(
                subject, message, to=[ad.author.email]
            )
            try:
                email.send()
            except BaseException:
                print('Ошибка')

            return redirect(next_url)
        else:
            print('Problem')

        return redirect(next_url)

@login_required
def confirmed_response(request, r_id):
    next_url = request.GET.get('next')

    resp = ResponseAd.objects.get(pk=r_id)
    resp.confirmed()

    subject = 'Подтверждение отклика'
    message = render_to_string('mails/confirmed_response.html', {
        'ad': resp.ad,
    })
    email = EmailMessage(
        subject, message, to=[resp.author.email]
    )
    try:
        email.send()
    except BaseException:
        print('Ошибка')

    return redirect(next_url)

@login_required
def rejected_response(request, r_id):
    next_url = request.GET.get('next')

    resp = ResponseAd.objects.get(pk=r_id)
    resp.rejected()

    return redirect(next_url)
