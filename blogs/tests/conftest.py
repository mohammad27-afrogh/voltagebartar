import pytest
from django.utils import timezone
from blogs.models import Blog, Category, CommentBlog


@pytest.fixture
def category():
    return Category.objects.create(
        name = 'TestBlog',
        slug = 'test_blog',
    )

@pytest.fixture
def blog_instance(category):
    return Blog.objects.create(
        name = 'blog1',
        slug = 'blog_1',
        category = category,
        short_description = 'This Is a Text Blog 1',
        description = 'Blog 1 is a Post flowers ',
    )