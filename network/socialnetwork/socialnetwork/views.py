
from django.urls import reverse
from django.views.generic import TemplateView

from django.shortcuts import redirect


class HomePage(TemplateView):
    template_name="index.html"