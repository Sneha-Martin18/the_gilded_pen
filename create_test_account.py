import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gilded_pen.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import BloggerProfile

def create_test_account():
    # Create test user
    username = 'testuser'
    email = 'test@example.com'
    password = 'testpass123'

    try:
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            print(f"Test user '{username}' already exists!")
            print("You can log in with:")
            print(f"Username: {username}")
            print(f"Password: {password}")
            return

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create blogger profile
        BloggerProfile.objects.create(
            user=user,
            bio='A test user exploring The Gilded Pen blog.'
        )

        print("Test account created successfully!")
        print("You can log in with:")
        print(f"Username: {username}")
        print(f"Password: {password}")

    except Exception as e:
        print(f"Error creating test account: {e}")

if __name__ == '__main__':
    create_test_account()
