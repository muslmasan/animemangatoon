from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics , viewsets
from .serializers import UserSerializer, ArticleSerilaizser
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Article
# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset= User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerilaizser
    permission_class = [IsAuthenticated]