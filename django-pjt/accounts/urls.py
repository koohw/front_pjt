from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile/<int:user_pk>/', views.get_profile, name='get_profile'),
    path('profile/<int:user_pk>/update/', views.update_profile, name='update_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
