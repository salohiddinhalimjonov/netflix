from rest_framework import serializers
from datetime import date
from rest_framework.exceptions import ValidationError
from .models import Movie, Actor, Comment
from django.contrib.auth.models import User
class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Actor
        fields='__all__'

    def validate_birth_date(self,data):


        if data.year < 1960:
            raise ValidationError('Birth Date can not be lower than 01.01.1960')


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'name', 'year', 'imdb', 'genre', 'actor', 'watched')

    def validate_imdb(self , value):
        if value == None or not value.endswith('.png'):
            raise ValidationError(detail='.mp4 file is required!')
        return value
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie', 'user', 'text', 'created_date')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username','password', 'first_name', 'last_name', 'is_active')
        write_only_fields = ('password',)#it will make sure passwords (actually: their hash we store) are not displayed,
        # while the overwritten create method ensures that the password is not stored in clear text, but as a hash.
        read_only_fields = ('id',)

        def create(self,validated_data):
            user = User.objects.create(
                email = validated_data['email'],
                username = validated_data['username'],
                first_name = validated_data['first_name'],
                last_name = validated_data['last_name'],
                is_active = True
            )
            user.set_password(validated_data['password'])#it will hash the password
            user.save()#and save it
            return user