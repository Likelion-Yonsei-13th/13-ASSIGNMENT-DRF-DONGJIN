from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content']
        read_only_fields = ['id']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'created_at', 'updated_at', 'content']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'created_at', 'updated_at', 'title', 'content', 'comments']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'comments']