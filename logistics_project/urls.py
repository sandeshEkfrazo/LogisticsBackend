from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.generic import RedirectView

admin.site.site_header = "LOGISTICS ADMIN"
admin.site.index_title = "Welcome to Logistics Admin Panle"
admin.site.site_title = "Adminlogistics"


urlpatterns = [
    #path('jet/', include('jet.urls', 'jet')),
    #path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('api/', include('logisticsapp.urls')),
    path('api/', include('userModule.urls')),
    path('api/', include('driverModule.urls')),
    path('api/', include('masters.urls')),
    # url(r'^$', serve,kwargs={'path': 'index.html'}),    
    # url(r'^(?!/?static/)(?!/?media/)(?P<path>.\..)$',RedirectView.as_view(url='/static/%(path)s', permanent=False)),
    

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
