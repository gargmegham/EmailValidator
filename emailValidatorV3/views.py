from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse

def error_404_handle(request, exception):
    messages.info(request, "You were accessing invalid URL")
    return HttpResponseRedirect(reverse("index"))