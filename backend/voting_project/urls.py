from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

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