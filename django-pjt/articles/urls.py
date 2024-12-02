from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "articles"
urlpatterns = [
    # 전체 게시글
    path('articles/', views.article_list, name='article_list'),
    # 게시글 디테일
    path('articles/<int:article_pk>/', views.article_detail, name='article_detail'),
    # 게시글 디테일 안 댓글
    path('articles/<int:article_pk>/comments/', views.comment_list_create, name='comment-list-create'),
    # 댓글 삭제
    path('articles/<int:article_pk>/comments/<int:comment_pk>/', views.comment_detail_delete, name='comment_detail_delete'),
    # 작성한 유저인지 확인
    path('current_user/', views.current_user, name='current_user'),
    # 게시글 수정
    path('articles/<int:article_pk>/update/', views.article_update, name='article_update'),
    # 게시글 삭제
    path('articles/<int:article_pk>/delete/', views.article_delete, name='article_delete'),

 ]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
