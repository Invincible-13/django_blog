from django.urls import path
from .views import index, BlogListView, BloggersListView, BlogDetailView, BloggerDetailView, AddCommentView, register, AddBlogPostView, BlogEditView, BlogDeleteView, CommentEditView, CommentDeleteView
from django.contrib.auth import views as user_views

urlpatterns = [
    path('', index, name='index'),
    path('blogs/', BlogListView.as_view(), name='blogs-list'),
    path('blogs/create/', AddBlogPostView.as_view(), name='blogs_post'),
    # path('blogs/create/', AddBlogPostView, name='blogs_post'),
    path('bloggers/', BloggersListView.as_view(), name='bloggers-list'),
    path('blogs/<int:pk>', BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/<int:pk>/edit/', BlogEditView.as_view(), name='blog_edit'),
    path('blogs/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
    path('blogs/<int:pk>/comment_edit/', CommentEditView.as_view(), name='comment_edit'),
    path('blogs/<int:pk>/comment_delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('bloggers/<int:pk>', BloggerDetailView.as_view(), name='blogger-detail'),
    path('blogs/<int:pk>/create/', AddCommentView.as_view(), name='add-comment'),
    # path('blogs/<int:pk>/create/', AddCommentView, name='add-comment'),
    path('register/', register, name='register'),
    path('login/', user_views.LoginView.as_view(), name='login'),
    path('logout/', user_views.LogoutView.as_view(), name='logout'),
]