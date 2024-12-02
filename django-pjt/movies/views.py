from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe, require_GET
from .models import Movie, Genre
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status



# Create your views here.
# 전체 영화 목록 페이지 조회
@require_safe
def index(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    context = {
        'movies': movies,
        'genres': genres,
    }
    return render(request, 'movies/index.html', context)

# 영화 목록 API 수정
@api_view(['GET'])
def movie_list(request):
    # 평점(vote_average)을 기준으로 내림차순 정렬
    movies = Movie.objects.all()  # '-vote_average'로 내림차순 정렬
    movies_data = [
        {
            'id': movie.tmdb_id,
            'title': movie.title,
            'overview': movie.overview,
            'poster_path': movie.poster_path,
            'backdrop_path': movie.backdrop_path,
            'vote_average': movie.vote_average,
            'vote_count': movie.vote_count,
            'release_date': movie.release_date,
        }
        for movie in movies
    ]
    return Response({'results': movies_data}, status=200)  # 'results'로 응답 구조 변경

@api_view(['GET'])
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, tmdb_id=movie_id)
    movie_data = {
        'id': movie.tmdb_id,
        'title': movie.title,
        'overview': movie.overview,
        'poster_path': movie.poster_path,
        'backdrop_path': movie.backdrop_path,
        'vote_average': movie.vote_average,
        'vote_count': movie.vote_count,
        'release_date': movie.release_date,
        'genres': [{'id': genre.id, 'name': genre.name} for genre in movie.genres.all()],  # 장르 정보 수정
    }
    return Response({'movie': movie_data}, status=200)  # 'movie'로 응답 구조 변경


# 필터링 된 영화 데이터 제공
@require_GET
def filter_genre(request):
    genre_id = request.GET.get('genre_id')

    if genre_id:
        movies = Movie.objects.filter(genres__id=genre_id)
    else:
        movies = Movie.objects.all()
    
    genres = Genre.objects.all()  # 장르도 함께 반환

    genres_data = [
        {'id': genre.id, 'name': genre.name}
        for genre in Genre.objects.all()
    ]
    
    movies_data = [
        {
        'id': movie.tmdb_id,  # tmdb_id를 id로 사용
        'title': movie.title,
        'release_date': movie.release_date,
        'popularity': movie.popularity,
        'vote_count': movie.vote_count,
        'vote_average': movie.vote_average,
        'overview': movie.overview,
        'poster_path': movie.poster_path,
        }
        for movie in movies
    ]
    return JsonResponse({'movies':movies_data, 'genres': genres_data})

# 영화 추천 페이지 조회
@require_safe
def recommended(request):
    pass

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, movie_id):
    movie = get_object_or_404(Movie, tmdb_id=movie_id)

    if movie.liked_by.filter(pk=request.user.pk).exists():
        # 이미 좋아요를 누른 경우 좋아요 취소
        movie.liked_by.remove(request.user)
        liked = False
    else:
        # 좋아요 추가
        movie.liked_by.add(request.user)
        liked = True

    like_count = movie.liked_by.count()

    # 좋아요 상태와 현재 좋아요 수를 응답으로 반환
    return Response(
        {"liked": liked, "like_count": like_count},
        status=status.HTTP_200_OK
    )