from django.shortcuts import render, get_object_or_404
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.views.generic import ListView
from django.db.models import Count
from taggit.models import Tag
from blog.forms import PostSendMailForm, CommentForm
from blog.models import Post, Comment
from blog.utils import post_share_mail


# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = "posts"
#     paginate_by = 3
#     template_name = "blog/post/post_list.html"


def all_post_by_tag(request, tag_slug=None):
    all_posts = Post.published.all()
    tag = get_object_or_404(Tag, slug=tag_slug)
    all_tagged_posts = all_posts.filter(tags__in=[tag])
    paginator = Paginator(all_tagged_posts, 3)
    page = request.GET.get("page")  # get the 'page' parameter from the url
    try:
        posts = paginator.page(page)  # get the particular posts for that page
    except PageNotAnInteger:
        posts = paginator.page(
            1
        )  # return the first page if the 'page' value dosent exist
    except EmptyPage:
        posts = paginator.page(
            paginator.num_pages
        )  # returns the last page if the 'page' value is out of range
    context = {"posts": posts, "page": page, "tag": tag}
    return render(request, "blog/post/post_list.html", context)


def post_list(request, tag_slug=None):
    """returns all posts that are published"""
    all_posts = Post.published.all()  # gets all published posts
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        all_posts = all_posts.filter(tags__in=[tag])
    paginator = Paginator(all_posts, 3)  # paginate the posts
    page = request.GET.get("page")  # get the 'page' parameter from the url
    try:
        posts = paginator.page(page)  # get the particular posts for that page
    except PageNotAnInteger:
        posts = paginator.page(
            1
        )  # return the first page if the 'page' value dosent exist
    except EmptyPage:
        posts = paginator.page(
            paginator.num_pages
        )  # returns the last page if the 'page' value is out of range
    context = {"posts": posts, "page": page, "tag": tag}
    return render(request, "blog/post/post_list.html", context)


def post_detail(request, post):
    "returns a single post that is published"
    post = get_object_or_404(
        Post, slug=post, status="published"
    )  # get particular object
    new_comment = None
    comments = post.comments.filter(active=True)  # get all active comments
    if request.method == "POST":
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        Comment.commentmanager.save_comment(comment_form, post)  # save comment

    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    context = {
        "comments": comments,
        "post": post,
        "comment_form": comment_form,
        "new_comment": new_comment,
        "similar_posts": similar_posts,
    }
    return render(request, "blog/post/post_detail.html", context)


def post_share(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, status="published")
    sent = False
    if request.method == "POST":
        form = PostSendMailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_share_mail(request, post, cd)
            sent = True
    else:
        form = PostSendMailForm()
    context = {"form": form, "post": post, "sent": sent}
    return render(request, "blog/post/share.html", context)
