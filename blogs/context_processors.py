from .models import Blog
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

def context_processors_blog(request):
    time_default = timezone.now()
    tow_month_ago = time_default - timedelta(days=60)

    blog_most_recent = Blog.objects.filter(Q(date_time_create__gte=tow_month_ago) &
                                              Q(date_time_create__lte=time_default)).order_by('id')

    return {'blog_most_recent': blog_most_recent}
