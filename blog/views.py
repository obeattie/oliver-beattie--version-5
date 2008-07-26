"""Views for the blog application."""
from django.views.generic import date_based as generic_date_based

from obeattie.blog import models as blog_models

def post_detail(request, year, month, day, slug):
    """The detail view for posts. Just a wrapper around django.views.generic.simple.date_based.object_detail
       for now (I don't like putting these in the urlconf directly as 1. They just don't feel right to me there,
       2. The urlconf gets awfully cluttered with all those dictionaries if I do that, and 3) Then I'd be *forced*
       to use named URL patterns for reverse URL matching)."""
    return generic_date_based.object_detail(
        request=request,
        queryset=blog_models.Post.objects.get_public(),
        date_field='published',
        year=year,
        month=month,
        day=day,
        slug=slug,
        month_format='%b',
        day_format='%d',
        template_name='blog/detail.html',
        template_object_name='post',
        allow_future=request.user.is_staff
    )
