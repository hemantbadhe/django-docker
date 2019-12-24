from django.contrib import admin
from django.urls import path, include

app_name = 'demo_app'

urlpatterns = [
    path('', include('demo_app.urls')),
    path('admin/', admin.site.urls),
]
