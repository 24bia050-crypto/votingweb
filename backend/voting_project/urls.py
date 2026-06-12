from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import FileResponse
import os

from django.conf import settings
from django.conf.urls.static import static

def serve_ads_txt(request):
    ads_txt_path = os.path.join(settings.BASE_DIR, 'ads.txt')
    return FileResponse(open(ads_txt_path, 'rb'), content_type='text/plain')

urlpatterns = [
    path('ads.txt', serve_ads_txt, name='ads_txt'),
    path('admin/', admin.site.urls),

    # Frontend pages
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('vote/', TemplateView.as_view(template_name='vote.html'), name='vote'),
    path('results/', TemplateView.as_view(template_name='results.html'), name='results'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
    path('admin-page/', TemplateView.as_view(template_name='admin.html'), name='admin_page'),

    # API
    path('api/', include('api.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)