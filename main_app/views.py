import datetime
import logging
import os
import pprint

from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import formset_factory, modelformset_factory, widgets
from django.http import HttpRequest, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from . import models, forms

logger = logging.getLogger(__name__)
pprint = pprint.PrettyPrinter(width=120)


def index(request: HttpRequest):
    context = dict(
        title='index',
        heading='heading',
    )
    return render(request, 'main_app/index.html', context)


@login_required
def form_view(request: HttpRequest, pk: int = None):
    form = forms.MainModelForm()

    if request.method == 'GET':
        if pk is not None:
            instance = get_object_or_404(models.MainModel, pk=pk)
            form = forms.MainModelForm(request.POST, request.FILES, instance=instance)

    if request.method == 'POST':
        logger.debug(request.POST)
        form = forms.MainModelForm(request.POST, request.FILES)
        if form.is_valid():
            if pk is None:
                logger.debug(form.cleaned_data)
                instance = models.MainModel(**form.cleaned_data)
                logger.debug(instance.file)
                instance.save()
                return redirect(reverse('main_app:form_view', args=[instance.pk]))

            else:
                instance = get_object_or_404(models.MainModel, pk=pk)
                form = forms.MainModelForm(request.POST, request.FILES, instance=instance)
                form.save()
                return redirect(reverse('main_app:form_view', args=[instance.pk]))

        else:
            if pk is not None:
                instance = get_object_or_404(models.MainModel, pk=pk)
                form = forms.MainModelForm(request.POST, request.FILES, instance=instance)

    context = dict(
        title='form_view',
        form=form,
    )
    return render(request, 'main_app/mainmodel_form.html', context)


def detail_view(request: HttpRequest, pk: int):
    instance = get_object_or_404(models.MainModel, pk=pk)  # type: models.MainModel
    logger.debug(type(instance))  # models.MainModel
    logger.debug(type(instance.file))  # FieldFile
    if os.path.isfile(instance.file.name):
        with instance.file.open() as f:
            contents = f.read()
            logger.debug(contents[:80])
    else:
        contents = ''
    context = dict(
        title='detail_view',
        object=instance,
        contents=contents,
    )
    return render(request, 'main_app/detail_view.html', context)


def long_count_streaming_http_response():
    start = datetime.datetime.now()
    for i in range(30):
        timer = datetime.datetime.now() - start
        logger.info(timer)
        yield f'{timer}<br>\n'


def streaming_http_test(_):
    return StreamingHttpResponse(long_count_streaming_http_response())


@login_required
def set_custom_permission(request: HttpRequest):
    logger.debug(request)
    # user = request.user  # type: User
    # logger.info(user)
    # content_type = ContentType()
    # user.user_permissions.add(Permission('banana', content_type=content_type))
    # logger.info(user.user_permissions)
    return redirect(reverse('main_app:index'))


@staff_member_required
@user_passes_test(lambda user: user.is_staff)
# @user_passes_test(lambda user: user.is_superuser)
def user_model_form(request: HttpRequest):
    UsersFormSet = modelformset_factory(
        model=User,
        extra=0,
        fields=[
            'username',
            # 'first_name',
            # 'last_name',
            # 'email',
            'is_active',
            # 'is_staff',
            'is_superuser',
            # 'password',
            # 'last_login',
            # 'groups',
            # 'user_permissions',
            # 'date_joined',
        ],
        widgets={
            'username': widgets.TextInput(
                attrs={
                    'readonly': True,
                },
            )
        },
        help_texts={
            'username': '',
            'is_active': '',
            'is_staff': '',
            'is_superuser': '',
        },
    )
    if request.method == 'POST':
        logger.debug(request.POST)
        formset = UsersFormSet(request.POST)
        # formset.forms.append(forms.CreateUsersForm(request.POST))
        if formset.is_valid():
            logger.info('formset.is_valid')
            for form in formset:
                logger.debug(form)
                logger.debug(dir(form))
                instance = form.instance
                # if instance.username == 'bad-user':
                #     instance.is_active = False
                #     instance.save()
                logger.debug(instance)
            formset.save()
            form = forms.CreateUsersForm(request.POST)
            if form.is_valid():
                logger.info('form.is_valid')
                logger.debug(form)
                email_addresses = form.cleaned_data.get('email_addresses')  # type: list
                if email_addresses:
                    logger.info(repr(email_addresses))
                    logger.info('create new users')
                formset.forms.append(forms.CreateUsersForm())

            else:
                logger.debug(form.errors)
                formset.forms.append(form)

        else:
            logger.info('NOT formset.is_valid')
            logger.debug(formset.errors)


    else:
        formset = UsersFormSet(
            queryset=User.objects.all().order_by('username'),
        )
        logger.debug(dir(formset))
        formset.forms.append(forms.CreateUsersForm())

    # form = forms.CreateUsersForm()
    # logger.info(form.fields.keys())
    # random_id = User.objects.make_random_password()
    # User.objects.create_user(random_id,random_id,random_id)
    # User.objects.create_user('tim', 'lennon@thebeatles.com', 'johnpassword')
    # User.objects.get_by_natural_key('bad-username') # exception if not found
    # users = User.objects.all().filter(username='admin')
    # users = User.objects.filter(username='bad-username')
    # logger.info(users)
    # if not users:
    #     logger.info('NO USERS FOUND')
    # users = User.objects.all()
    # for user in users:  # type: User
    #     logger.info(type(user))
    context = dict(
        title='user_model_form',
        formset=formset,
    )
    return render(request, 'base-formset.html', context)


class MainModelListView(generic.ListView):
    model = models.MainModel
    ordering = '-id'
    paginate_by = 20
    extra_context = dict(title='CreateView')


class MainModelCreateView(generic.CreateView):
    model = models.MainModel
    fields = '__all__'
    success_url = reverse_lazy('main_app:index')
    extra_context = dict(title='CreateView')


class MainModelDetailView(generic.DetailView):
    model = models.MainModel
    extra_context = dict(title='DetailView')


class MainModelUpdateView(generic.UpdateView):
    model = models.MainModel
    fields = '__all__'
    success_url = reverse_lazy('main_app:index')
    extra_context = dict(title='UpdateView')


class MainModelDeleteView(generic.DeleteView):
    model = models.MainModel
    success_url = reverse_lazy('main_app:index')
    extra_context = dict(title='DeleteView')
