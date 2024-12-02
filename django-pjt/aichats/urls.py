# movie/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 'get-scene-location/' 경로로 들어온 요청을 get_scene_location 뷰에서 처리
    path('get-scene-location/', views.get_scene_location, name='get_scene_location'),
]
