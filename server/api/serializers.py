import re
from rest_framework import serializers 
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

# Есть подозрение, что это жуткий велосипед,
# но лучшего способа внедрить repeat_password не нашел
class RegisterDataSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('This username is already taken.')

        if len(username) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters")
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]+$', username):
            raise serializers.ValidationError("Username may only contain latin letters, digits, "
                "underscore and must begin with a letter.")

        return username


    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    def validate(self, data):
        password = data.get('password')
        repeat_password = data.get('repeat_password')

        if password != repeat_password:
            raise serializers.ValidationError({'repeat_password': "Passwords don't match."})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.get('username')
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        return user

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'