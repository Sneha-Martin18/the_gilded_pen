import os
import django
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gilded_pen.settings')
django.setup()

from blog.models import Category, Tag, BloggerProfile, Post

def create_sample_content():
    # Create categories
    categories = [
        {
            'name': 'Technology',
            'description': 'Articles about programming, software development, and tech trends.'
        },
        {
            'name': 'Writing Tips',
            'description': 'Advice and guidelines for improving your writing skills.'
        },
        {
            'name': 'Personal Growth',
            'description': 'Stories and insights about personal development and learning.'
        }
    ]

    created_categories = []
    for cat in categories:
        category = Category.objects.create(
            name=cat['name'],
            slug=slugify(cat['name']),
            description=cat['description']
        )
        created_categories.append(category)
        print(f"Created category: {category.name}")

    # Create tags
    tags = ['Python', 'Django', 'Web Development', 'Creativity', 'Learning', 'Productivity']
    created_tags = []
    for tag_name in tags:
        tag = Tag.objects.create(
            name=tag_name,
            slug=slugify(tag_name)
        )
        created_tags.append(tag)
        print(f"Created tag: {tag.name}")

    # Get or create a superuser
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print("Created superuser: admin")

    # Create blogger profile
    blogger_profile, created = BloggerProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'bio': 'A passionate writer and technology enthusiast sharing insights about programming and personal growth.',
            'website': 'https://example.com'
        }
    )
    if created:
        print(f"Created blogger profile for: {admin_user.username}")

    # Create sample blog posts
    posts = [
        {
            'title': 'Welcome to The Gilded Pen',
            'content': """
Welcome to The Gilded Pen, a space where words come to life and ideas flourish. This blog is dedicated to sharing knowledge, experiences, and insights across various topics.

In this community, we believe in the power of writing to inspire, educate, and connect people. Whether you're a seasoned writer or just starting your journey, you'll find valuable resources and engaging discussions here.

Stay tuned for upcoming articles on technology, writing tips, and personal growth. Don't forget to join our community by creating an account and sharing your thoughts in the comments section.

Happy reading and writing!
            """.strip(),
            'category': 'Personal Growth',
            'tags': ['Creativity', 'Writing']
        },
        {
            'title': 'Getting Started with Django Web Development',
            'content': """
Django is a high-level Python web framework that enables rapid development of secure and maintainable websites. Built by experienced developers, Django takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

In this post, we'll explore:
- Why choose Django for web development
- Setting up your first Django project
- Understanding the MTV (Model-Template-View) architecture
- Best practices for Django development

Stay tuned for more detailed tutorials on Django development!
            """.strip(),
            'category': 'Technology',
            'tags': ['Python', 'Django', 'Web Development']
        }
    ]

    for post_data in posts:
        post = Post.objects.create(
            title=post_data['title'],
            slug=slugify(post_data['title']),
            author=admin_user,
            content=post_data['content'],
            category=Category.objects.get(name=post_data['category']),
            published_date=timezone.now()
        )
        for tag_name in post_data['tags']:
            tag = Tag.objects.get(name=tag_name)
            post.tags.add(tag)
        print(f"Created post: {post.title}")

if __name__ == '__main__':
    print("Creating sample content...")
    create_sample_content()
    print("Sample content creation completed!")
