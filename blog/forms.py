from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.text import slugify
from .models import Comment, Post, BloggerProfile

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            }),
        }
        labels = {
            'text': 'Comment'
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your blog post here...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control'
            })
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if self.instance.pk is None:  # Only for new posts
            slug = slugify(title)
            if Post.objects.filter(slug=slug).exists():
                raise forms.ValidationError('A post with this title already exists. Please choose a different title.')
        return title

    def save(self, commit=True):
        post = super().save(commit=False)
        post.slug = slugify(post.title)
        if commit:
            post.save()
            self.save_m2m()  # Save many-to-many relationships (tags)
        return post

class BloggerProfileForm(forms.ModelForm):
    class Meta:
        model = BloggerProfile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write something about yourself...'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
