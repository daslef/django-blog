from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

from blog.models import Post


def post_list(request):
    posts = Post.approved.all()

    paginator = Paginator(posts, 1)
    current_page = request.GET.get("page", 1)
    current_posts = paginator.page(current_page)

    return render(request, "blog/post/list.html", {"posts": current_posts})


def post_detail(request, year, month, day, slug):
    try:
        post = Post.approved.filter(
            published__year=year,
            published__month=month,
            published__day=day,
            slug=slug,
        ).get()

    except Post.DoesNotExist:
        raise Http404("No post found")

    return render(request, "blog/post/detail.html", {"post": post})
