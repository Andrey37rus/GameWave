from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView


class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'
