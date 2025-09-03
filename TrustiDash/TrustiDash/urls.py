
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("signup.urls")),
    path('tdapp/',include("tdapp.urls")),
    path("ml/",include("ml.urls")),
]
