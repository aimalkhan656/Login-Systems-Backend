from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello! API is working. Visit /admin/ or /api/")

urlpatterns = [
    path('', home),  # Add this line
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
]
