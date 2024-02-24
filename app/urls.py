from django.urls import include, path

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", include("validator.urls"))
]

handler404 = views.error_404_handle
