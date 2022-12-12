from rest_framework import serializers
from .models import *
from .fields import *


class CustomUserSerializer(serializers.ModelSerializer):

    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    email = serializers.EmailField(required=True)
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'followers',
            'following',
         ) 
        
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance

    def get_following(self, obj):
        return FollowingSerializer(obj.users_followed.all(),many=True).data

    def get_followers(self,obj):
        return FollowerSerializer(obj.users_following.all(), many=True).data



class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.ReadOnlyField(source='comment_author.username')
    class Meta:
        model = Comment
        fields = (
                'id',
                'comment',
                'comment_author',
                'created_at', 
                'post',
                'commented_by'
                )


class PostSerializer(serializers.ModelSerializer):
    post_author = ForeignKeyField(queryset=CustomUser.objects.all(), serializer=CustomUserSerializer)
    comments = CommentSerializer(many=True,read_only=True)
    class Meta:
        model = Post
        fields = (
                'id',
                'body',
                'post_author',
                'category',
                'created_at',
                'comments',
                'post_author'
                )


class FollowSerializer(serializers.ModelSerializer):
    followers = ForeignKeyField(queryset=CustomUser.objects.all(), serializer=CustomUserSerializer)
    followers = ForeignKeyField(queryset=CustomUser.objects.all(), serializer=CustomUserSerializer)
    class Meta:
        model = Follow
        fields = (
                'following', 
                'followers'
                )


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = (
                'id',
                'followers',
                'created_at'
                )


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = (
            'id',
            'following',
            'created_at',
        )


# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         fields = "__all__"

