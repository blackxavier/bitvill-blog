from django.shortcuts import render, get_object_or_404
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.views.generic import ListView
from blog.models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/post_list.html"


# def post_list(request):
#     "returns all posts that are published"
#     all_posts = Post.published.all()  # gets all published posts
#     paginator = Paginator(all_posts, 3)  # paginate the posts
#     page = request.GET.get("page")  # get the 'page' parameter from the url
#     try:
#         posts = paginator.page(page)  # get the particular posts for that page
#     except PageNotAnInteger:
#         posts = paginator.page(
#             1
#         )  # return the first page if the 'page' value dosent exist
#     except EmptyPage:
#         posts = paginator.page(
#             paginator.num_pages
#         )  # returns the last page if the 'page' value is out of range
#     context = {"posts": posts, "page": page}
#     return render(request, "blog/post/post_list.html", context)


def post_detail(request, post):
    "returns a single post that is published"
    post = get_object_or_404(Post, slug=post, status="published")
    context = {"post": post}
    return render(request, "blog/post/post_detail.html", context)
