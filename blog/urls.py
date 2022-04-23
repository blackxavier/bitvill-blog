from django.urls import path
from blog import views
from .feeds import LatestPostsFeed

app_name = "blog"


urlpatterns = [
    # post views
    path("", views.post_list, name="post_list"),
    path("feeds/", LatestPostsFeed(), name="post_feed"),
    path("search/", views.post_search, name="post_search"),
    path("posts/tags/<slug:tag_slug>/", views.all_post_by_tag, name="post_list_by_tag"),
    path(
        "<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    path(
        "share/<slug:post_slug>/",
        views.post_share,
        name="post_share",
    ),
]
