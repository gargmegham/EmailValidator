from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse


def error_404_handle(request, exception):
    messages.info(request, "You were accessing invalid URL")
    return HttpResponseRedirect(reverse("index"))
