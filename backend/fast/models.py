from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    post_title = models.CharField (max_length=32, null=False, blank=False, verbose_name='Post Title' )
    post_details = models.CharField (max_length=255, null=False, blank=False, verbose_name='Post Details' )
    post_posted_by = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_user_related', on_delete=models.CASCADE)
    added_date_time = models.DateTimeField(auto_now_add=True, blank=True)