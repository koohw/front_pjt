from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from .models import Article, Comment



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    
    if request.method == 'GET':
        # 게시글 조회
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        comments = Comment.objects.filter(article=article)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # article과 user를 직접 설정
            serializer.save(article=article, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # 에러 로그 확인
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 삭제기능
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def comment_detail_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, article__pk=article_pk)

    # 작성자인지 확인
    if request.user != comment.user:
        return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({"detail": "댓글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response({"username": request.user.username})

# 게시글 수정
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def article_update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    # 작성자인지 확인
    if request.user != article.user:
        return Response({"detail": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    # 수정 처리
    serializer = ArticleSerializer(article, data=request.data, partial=True)  # 부분 업데이트 허용
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)

# 게시글 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def article_delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    # 작성자 확인
    if request.user != article.user:
        return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    # 삭제
    article.delete() # 댓글도 같이 삭제
    return Response({"detail": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


