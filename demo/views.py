from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse

# Create your views here.
def HomeView(request):
    return render(request, "home.html")
    # return HttpResponse("Hello, world. You're at the polls index.")
