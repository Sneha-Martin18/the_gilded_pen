from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .models import Post, BloggerProfile, Category, Tag, Comment
from .forms import CommentForm, SignUpForm, PostForm, BloggerProfileForm

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/home.html'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'The Gilded Pen'
        return context

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/index.html'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About The Gilded Pen'
        return context

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-published_date']
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context

class BloggerListView(LoginRequiredMixin, ListView):
    model = BloggerProfile
    template_name = 'blog/blogger_list.html'
    context_object_name = 'bloggers'
    login_url = 'login'
    redirect_field_name = 'next'

class BloggerDetailView(LoginRequiredMixin, DetailView):
    model = BloggerProfile
    template_name = 'blog/blogger_detail.html'
    context_object_name = 'blogger'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.object.user).order_by('-published_date')
        return context

class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'blog/category_detail.html'
    context_object_name = 'category'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all().order_by('-published_date')
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class TagDetailView(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'blog/tag_detail.html'
    context_object_name = 'tag'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all().order_by('-published_date')
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = 'login'
    redirect_field_name = 'next'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        messages.success(self.request, 'Your blog post has been created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_queryset(self):
        # Only allow users to edit their own posts
        return Post.objects.filter(author=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Your blog post has been updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    login_url = 'login'
    redirect_field_name = 'next'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class BloggerProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = BloggerProfile
    form_class = BloggerProfileForm
    template_name = 'blog/blogger_form.html'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_object(self, queryset=None):
        return self.request.user.bloggerprofile

    def get_success_url(self):
        return reverse_lazy('blog:blogger_detail', kwargs={'username': self.request.user.username})

@login_required(login_url='login')
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', slug=post.slug)
    
    return redirect('blog:post_detail', slug=post.slug)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            BloggerProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Welcome to The Gilded Pen! Your account has been created successfully.')
            return redirect('blog:home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
