from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):

        return super(PublishedManager, self).get_queryset().filter(status="published")


class Post(models.Model):
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
    objects = models.Manager() #default manager
    published = PublishedManager()#custom manager for published posts

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
