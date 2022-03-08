from django.urls import path
from blog import views

app_name = "blog"


urlpatterns = [
    # post views
    path("", views.PostListView.as_view(), name="post_list"),
    path(
        "<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
]
