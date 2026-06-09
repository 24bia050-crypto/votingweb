from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
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
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'   
)