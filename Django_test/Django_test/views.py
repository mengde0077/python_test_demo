#coding: utf-8
from django.shortcuts import render
from django.http import HttpRequest

def index(request):
    return render(request, 'index.html')
