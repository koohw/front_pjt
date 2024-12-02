from rest_framework import serializers
from .models import Article, Comment


# 댓글 직렬화
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'content': {'required': True},
            'article': {'read_only': True},
        }
        read_only_fields = ('user',)  # `article`은 제거



# 게시글 목록 직렬화 (댓글 제외)
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'created_at', 'updated_at')


# 게시글 상세 직렬화 (댓글 포함)
class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    # 댓글을 포함하도록 nested serializer 추가 
    comments = CommentSerializer(many=True, read_only=True, source='comment_set') 

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)  # 게시글 작성자는 자동 설정
