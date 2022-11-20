from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class BlogAuthor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField()

    class Meta:
        ordering = ['user', 'bio']

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])

class Blog(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_posted = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail',args=[str(self.id)])

class BlogComment(models.Model):
    description = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('blog-detail',args=[str(self.blog.id)])


