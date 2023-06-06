import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from . import models, forms

logger = logging.getLogger(__name__)


def home(request: HttpRequest):
    context = dict(
        title='home',
        heading='heading',
    )
    return render(request, 'main_app/home.html', context)


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
    logger.debug(type(instance)) # models.MainModel
    logger.debug(type(instance.file))  # FieldFile
    with instance.file.open() as f:
        contents = f.read()
        logger.debug(contents[:80])
    context = dict(
        title='detail_view',
        object=instance,
        contents=contents,
    )
    return render(request, 'main_app/detail_view.html', context)


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
