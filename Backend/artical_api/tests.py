from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Article, Character
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APIClient

def obtain_access_token(self):
        response = self.client.post(reverse('get_token'), {
            'username': 'testuser',
            'password': 'testpass',
        })
        return response.data['access']

def create_article(self,access_token):
    self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    data = {
        'title': 'test_article',
        'description': 'test_article_description.',
        'characters': [{
            'name':'test_character',
            'description':'test_character_description.',
            }],
     }
    response = self.client.post(self.article_url, data, format='json')
    return response


class ArticleAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.character = Character.objects.create(name='test_character', description='test_character_description.')
        self.article = Article.objects.create(title="Original Title", description="Content", author=self.user)
        self.article_url = reverse('article-list') 
    
    def test_list_article(self):
         response = self.client.get(reverse('article-list'))
         articles = Article.objects.all().count()

         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(len(response.data), articles)

    def test_create_article(self):
        access_token = obtain_access_token(self)
        response = create_article(self, access_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        article = Article.objects.get(title='test_article')
        self.assertEqual(article.description, 'test_article_description.')
        self.assertIn(self.character, article.characters.all())

    def test_unauthenticated_create_article(self):
        data = {
            'title': 'Another Test Article',
            'description': 'This should not be created.',
            'characters': [self.character.id],
        }
        response = self.client.post(self.article_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_article(self):
         access_token = obtain_access_token(self)
         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
         data = {
              'characters': [{
                   'name':'added name',
                   'description':'added description',
                   }],}
         article_id = self.article.id
         url = reverse('article-detail', args=[article_id])
         response = self.client.patch(url, data, format='json')
         
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(response.data['characters'][0]['name'], 'added name')
         self.assertIn('characters', response.data)

    def test_delete_article(self):
         access_token = obtain_access_token(self)
         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
         article_id = self.article.id

         url = reverse('article-detail', args=[article_id])
         response = self.client.delete(url)

         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
         