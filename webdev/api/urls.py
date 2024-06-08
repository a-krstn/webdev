from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'cats', views.CategoryViewSet, basename='category')
router.register(r'tags', views.TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('follow/<int:pk>/',
         views.CreateUserFollowingAPIView.as_view(),
         name='follow')
]
