from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('receitas_app.urls')),
    path('admin/', admin.site.urls),
]
