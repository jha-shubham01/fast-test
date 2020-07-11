from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Post


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': ('User account is disabled.'),
        'invalid_credentials': ('Unable to login with provided credentials.'),
    }

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("id", "post_title", "post_details", "post_posted_by")

    def get_post_posted_by(self, obj):
        print(self.request.user)
        return obj.post_posted_by.post_posted_by


class PostListSerializer(serializers.ModelSerializer):
    post_posted_by = serializers.SlugRelatedField(read_only=True, slug_field='email')

    class Meta:
        model = Post
        fields = ("id", "post_title", "post_details", "post_posted_by")