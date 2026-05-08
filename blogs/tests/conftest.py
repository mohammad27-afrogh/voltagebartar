import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from blogs.models import Blog, Category, CommentBlog

@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        username = 'testerblog',
        password = 'password123456',
        email = 'userblog@test.com'
    )


@pytest.fixture
def category():
    return Category.objects.create(
        name = 'TestBlog',
        slug = 'Test_Blog',
    )

@pytest.fixture
def blog_instance(category, user):
    return Blog.objects.create(
        user = user,
        name = 'blog1',
        slug = 'blog_1',
        category = category,
        short_description = 'This Is a Text Blog 1',
        description = 'Blog 1 is a Post flowers ',
    )