from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    birthday = models.DateField(null=True)

    def __str__(self):
        return self.username

        """ 
        only pull in the PROVIDED DJANGO USER FIELDS that are going to be used in creating a user, 
        and then add your extended fields,
        '__all__' pulls in all fields and creates an error for the validation step below
        """
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class Post(models.Model):
    body = models.CharField(max_length=550)
    created_at = models.DateField(auto_now_add=True)
    post_author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='user_post')
    category = models.CharField(max_length=225, default=None, blank=True, null=True)

    def __str__ (self):
        return self.body

class Comment(models.Model):
    comment_author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment

class Follow(models.Model):
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=False, related_name='users_followed')
    followers = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=False, related_name='users_following')
    created_at = models.DateField(auto_now_add=True, db_index=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['following','followers'],  name="unique_followers")
        ]

        ordering = ["-created_at"]

        def __str__(self):
            return self.followers


