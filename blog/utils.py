from django.core.mail import send_mail
import random
import string
from django.db import transaction



@transaction.atomic()
def post_share_mail(request, post, cd):
    post_url = request.build_absolute_uri(post.get_absolute_url())
    subject = f"{post.author.email} recommends you read " f"{post.title}"
    message = (
        f"Read {post.title} at {post_url}\n\n"
        f"{post.author.email}'s comments: {cd['comments']}"
    )
    send_mail(subject, message, "admin@myblog.com", [cd["to"]])


@transaction.atomic()
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str