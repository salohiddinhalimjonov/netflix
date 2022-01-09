from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, ActorViewSet, CommentViewSet, RegisterViewSet
from rest_framework.authtoken import views

router = DefaultRouter()
router.register('movies', MovieViewSet, basename='movies')
router.register('actors', ActorViewSet, basename='actors')
router.register('comments', CommentViewSet, basename='comments')
router.register('register', RegisterViewSet, basename='register')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.obtain_auth_token),
]