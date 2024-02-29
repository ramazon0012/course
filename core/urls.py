from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('users/', include('allauth.urls')),
    path('users/', include('allauth.socialaccount.urls')),  # Include Socialaccount URLs for social authentication
    path('social/', include('allauth.socialaccount.urls')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('app.urls')),
)
if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL,
 document_root=settings.MEDIA_ROOT)
 urlpatterns += static(settings.STATIC_URL,
 document_root=settings.STATIC_ROOT)