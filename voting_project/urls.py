from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Backend is working!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),  # 🔥 TEST FIX
    path('api/', include('api.urls')),
]