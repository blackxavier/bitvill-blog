from django.core.mail import send_mail


def post_share_mail(request, post, cd):
    post_url = request.build_absolute_uri(post.get_absolute_url())
    subject = f"{post.author.email} recommends you read " f"{post.title}"
    message = (
        f"Read {post.title} at {post_url}\n\n"
        f"{post.author.email}'s comments: {cd['comments']}"
    )
    send_mail(subject, message, "admin@myblog.com", [cd["to"]])
