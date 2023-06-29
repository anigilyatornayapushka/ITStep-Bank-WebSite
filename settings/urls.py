# Django
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import (
    include,
    path,
)
from django.conf import settings


urlpatterns = [
    # Admin panel
    path('admin/', include('auths.authadmin.urls')),
    path('admin/', admin.site.urls),

    # User processing
    path('api/v1/auth/', include('auths.urls')),

    # Card and transactions processing
    path('api/v1/bank/', include('bank.urls')),

    # All routes for site users
    path('', include('frontend.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# DEBUG TOOLBAR
# if settings.DEBUG is True:

    # urlpatterns += [
    #     # Debug-toolbar when in development mode
    #     path('__debug__/', include('debug_toolbar.urls')),
    # ]
