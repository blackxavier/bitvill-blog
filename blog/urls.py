from django.urls import path
from blog import views

app_name = "blog"


urlpatterns = [
    # post views
    path("", views.post_list, name="post_list"),
    path("tags/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    path(
        "<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    path(
        "share/<int:post_id>/",
        views.post_share,
        name="post_share",
    ),
]
