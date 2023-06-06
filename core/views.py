import logging

from django.http import HttpRequest
from django.shortcuts import render

logger = logging.getLogger(__name__)


def handle404(request: HttpRequest, path: str):
    context = dict(
        title='HELLO WORLD!',
        path=path,
    )
    return render(request, '404.html', context, status=404)
