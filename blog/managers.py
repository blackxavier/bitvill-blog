from django.db import models
from django.db import transaction


class CommentManager(models.Manager):
    """custom model manager"""

    @transaction.atomic()
    def save_comment(self, comment_form, post):
        """method to save method"""
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False, post=post)
            new_comment.post = post
            new_comment.save()
            return new_comment


class PublishedManager(models.Manager):
    """model manager that returns all published posts"""

    @transaction.atomic()
    def get_queryset(self):

        return super(PublishedManager, self).get_queryset().filter(status="published")
