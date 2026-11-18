from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from todo.sitemaps import TaskSitemap 

sitemaps = {
    'tasks': TaskSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', include('todo.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', RedirectView.as_view(url='/todo/', permanent=True)),
]
