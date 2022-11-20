from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Blog, BlogAuthor, BlogComment
from .forms import CommentForm, BlogForm
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied

# Create your views here.
def index(request):
    return render(request, 'blog/index.html', {})

class BlogListView(ListView):
    model = Blog
    paginate_by = 5
    def get_queryset(self):
        return Blog.objects.all().order_by('-date_posted')

class BlogDetailView(DetailView):
    model = Blog

class BloggersListView(ListView):
    model = BlogAuthor

class BloggerDetailView(DetailView):
    model = BlogAuthor

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form':form})

class AddCommentView(CreateView):
    model = BlogComment
    fields = ['description']
    template_name = 'blog/add_comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return super(AddCommentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'],})

class AddBlogPostView(CreateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog/add_blog.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
    #     return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        # form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return super(AddBlogPostView, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog-detail', args=(self.object.id,))

class BlogEditView(UpdateView):
    model = Blog
    fields = ['title', 'content']

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise Http404("You are not allowed to edit this Post")
        return super(BlogEditView, self).dispatch(request, *args, **kwargs)

class BlogDeleteView(DeleteView):
    model = Blog

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied()
        return super(BlogDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blogs-list')

class CommentEditView(UpdateView):
    model = BlogComment
    fields = ['description']

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied()
        return super(CommentEditView, self).dispatch(request, *args, **kwargs)
        

class CommentDeleteView(DeleteView):
    model = BlogComment

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author == self.request.user or obj.blog.author == self.request.user: 
            return super(CommentDeleteView, self).dispatch(request, *args, **kwargs)
            
        raise PermissionDenied()
        

    def get_success_url(self):
        return reverse('blog-detail', args=(self.object.blog.id,))

# @login_required
# def AddBlogPostView(request):
#     # blog_post = get_object_or_404(Blog, pk=pk)
#     if request.method == 'POST':
#         form = BlogForm(request.POST)
#         if form.is_valid():
#             new_blog = form.save(commit=False)
#             new_blog.author = request.user
#             new_blog.save()
#             return HttpResponseRedirect(reverse('blog-detail', args=[new_blog.id]))
#     else:
#         form = BlogForm()

#     return render(request, 'blog/add_comment.html', {'form': form})

# @login_required
# def AddCommentView(request, pk):
#     blog_post = get_object_or_404(Blog, pk=pk)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.blog = blog_post
#             new_comment.author = request.user
#             new_comment.save()
#             return HttpResponseRedirect(reverse('blog-detail', args=[blog_post.id]))
#     else:
#         form = CommentForm()

#     return render(request, 'blog/add_comment.html', {'form': form})
