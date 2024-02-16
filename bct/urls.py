from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls", namespace='accounts')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.home_page, name='home_page'),
    path('volunteer/', views.volunteers_needed, name="volunteer"),
    path('faqs/', views.faqs, name="faqs"),
    path('team/', views.team, name="team"),
    path('customers/', views.customers, name="customers"),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('terms/', views.tandc_policy, name='termsandconditions'),
    path('disclaimer/', views.disclaimer_policy, name='disclaimer'),
    path('cookie/', views.cookie_policy, name='cookie'),
    path('contact/', views.contact_me, name='contact'),
    path('donate/', include('donate.urls', namespace='donate')),
    path('extensions/', include('extensions.urls', namespace='extensions')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)