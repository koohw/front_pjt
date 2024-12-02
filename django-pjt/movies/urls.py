from django.urls import path
from . import views

app_name = "movies"
urlpatterns = [
    # 전체 영화 목록 페이지 조회
    path("", views.movie_list, name="movie_list"),
    # 영화 상세 페이지 조회
    path("<int:movie_id>/", views.movie_detail, name="movie_detail"),
    # 필터링 된 영화 데이터 제공
    path("filter-genre/", views.filter_genre, name="filter_genre"),
    # 영화 추천 페이지 조회
    path("recommended/", views.recommended, name="recommended"),
    # 영화 좋아요 기능
    path("<int:movie_id>/like/", views.toggle_like, name="toggle_like"),
]
