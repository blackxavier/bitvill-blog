from django.db import models

class CommentManager(models.Manager):
    """custom model manager"""

    def save_comment(self, comment_form, post):
        """method to save method"""
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False, post=post)
            new_comment.post = post
            new_comment.save(update_fields=['post'])
            return new_comment

class PublishedManager(models.Manager):
    """model manager that returns all published posts"""

    def get_queryset(self):

        return super(PublishedManager, self).get_queryset().filter(status="published")