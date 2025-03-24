from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('bloggers/', views.BloggerListView.as_view(), name='blogger_list'),
    path('blogger/<str:username>/', views.BloggerDetailView.as_view(), name='blogger_detail'),
    path('profile/edit/', views.BloggerProfileUpdateView.as_view(), name='profile_edit'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('signup/', views.signup, name='signup'),
]
