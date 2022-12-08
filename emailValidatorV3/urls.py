from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('validator.urls'))
]

handler404 = views.error_404_handle