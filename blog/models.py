from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """model manager that returns all published posts"""

    def get_queryset(self):

        return super(PublishedManager, self).get_queryset().filter(status="published")


class Post(models.Model):
    """Post Model"""

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(_("Blog title"), max_length=250)
    slug = models.SlugField(_("Post slug"), max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField(_("Blog body"))
    status = models.CharField(
        _("Blog status"), max_length=20, choices=STATUS_CHOICES, default="draft"
    )
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()  # default manager
    published = PublishedManager()  # custom manager for published posts
    tags = TaggableManager() #tag manager
    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        "returns canonical url for each posts"
        return reverse(
            "blog:post_detail",
            args=[
                self.slug,
            ],
        )


class CommentManager(models.Manager):
    """custom model manager"""

    def save_comment(self, comment_form, post):
        """method to save method"""
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False, post=post)
            new_comment.post = post
            new_comment.save()
            return new_comment


class Comment(models.Model):
    """Comment model"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    objects = models.Manager
    commentmanager = CommentManager()

    class Meta:
        ordering = ("-created",)
        db_table = "Comments"

    def __str__(self):
        return f"Comment by {self.email} on {self.post.title}"
