import pytest

from blogs.models import Blog, CommentBlog

@pytest.mark.django_db
def test_blog_creation_success(blog_instance, category):
    assert blog_instance.category == category


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
