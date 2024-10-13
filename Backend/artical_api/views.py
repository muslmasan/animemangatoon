from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics , viewsets
from .serializers import UserSerializer, ArticleSerilaizser
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Article
from .permission import AllowGetOnly
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

# Create your views here.
@method_decorator(ratelimit(key='user', rate='3/m', method='POST', block=True), name='dispatch')
class CreateUserView(generics.CreateAPIView):
    queryset= User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@method_decorator(ratelimit(key='user', rate='5/m', method='POST', block=True), name='dispatch')
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerilaizser
    permission_classes = [AllowGetOnly]

    def perform_create(self, serializer):

        serializer.save(author=self.request.user)