from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Article, Character


class UserSerializer(serializers.ModelSerializer):

    title = serializers.CharField(required=True)
    descrition = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password":{"write_only":True}}
    
    def create(self, data):
        user = User.objects.create_user(**data)
        return user

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'name', 'description']

class ArticleSerilaizser(serializers.ModelSerializer):
    characters = CharacterSerializer(many=True)
    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'characters', 'author']
        extra_kwargs = {'author':{'read_only': True}}
    
    def create(self, validated_data):
        characters_data = validated_data.pop('characters')
        article = Article.objects.create(**validated_data)
        for character_data in characters_data:
            character, created = Character.objects.get_or_create(**character_data)
            article.characters.add(character)
        return article
    
    def update(self, instance, validated_data):
        characters_data = validated_data.pop('characters', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        if characters_data is not None:
            instance.characters.clear()
            for character_data in characters_data:
                character, created = Character.objects.get_or_create(**character_data)
                instance.characters.add(character)
        return instance