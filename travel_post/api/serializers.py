from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','email','username','password','first_name','last_name',) 
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance


class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.ReadOnlyField(source='comment_author.username')
    class Meta:
        model = Comment
        fields = ('id','comment','comment_author','created_at', 'post','commented_by')


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True,read_only=True)
    class Meta:
        model = Post
        fields = ('id','body','post_author','category','created_at','comments')

class FollowSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('following', 'followers', 'status')
