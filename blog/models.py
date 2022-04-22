from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from taggit.managers import TaggableManager
from blog.managers import CommentManager, PublishedManager
from blog.utils import get_random_string
from django.db.models.signals import pre_save
from django.db import transaction


class Post(models.Model):
    """Post Model"""

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(_("Blog title"), max_length=250)
    slug = models.SlugField(_("Post slug"), max_length=250,unique=True,blank=True,null=False)
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
    tags = TaggableManager()  # tag manager

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


@transaction.atomic()
def create_slug(instance, new_slug=None):
    """
    Create and validate slug duplication
    """
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    else:
        qs = Post.objects.filter(slug=slug).order_by("-id")
        exist = qs.exists()
        if exist:
            generated_string = get_random_string(4)
            slug = slug + "-" + generated_string
    return slug


def pre_save_post_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_reciever, sender=Post)


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
