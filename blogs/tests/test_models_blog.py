import pytest
from django.contrib.auth import get_user_model

from blogs.models import Blog, CommentBlog

@pytest.mark.django_db
def test_blog_creation_success(blog_instance, category):
    assert blog_instance.category == category

@pytest.mark.django_db
def test_blog_creation_with_missing_optional_fields(category):
    blog_test = Blog.objects.create(
        name = 'blog test flower',
        slug = 'blog_flo',
        category = category,
        short_description = 'blog test flower sanseveria',
    )

@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        username = 'testerblog',
        password = 'password123456',
        email = 'userblog@test.com'
    )

@pytest.mark.django_db
def test_blog_comment_creation(blog_instance, user):
    comment = CommentBlog.objects.create(
        blog = blog_instance,
        user = user,
        body_comment = 'Gret blog fast shipping'
    )

    assert comment.blog == blog_instance
    assert comment.user == user
    assert blog_instance.comments.count() == 1
    assert blog_instance.get_absolute_url() == f'/blogs/{blog_instance.slug}/'
