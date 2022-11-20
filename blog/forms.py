from django.forms import ModelForm
from .models import BlogComment, Blog

class CommentForm(ModelForm):

    class Meta:
        model = BlogComment
        fields = ['description']

class BlogForm(ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'content']