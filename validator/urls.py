from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("delete/", views.deleteFile, name="deleteFile"),
    path("download/", views.downloadFile, name="downloadFile"),
    path("process/", views.processFile, name="processFile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
