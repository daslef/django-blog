from typing import Any

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from blog.forms import CommentForm, EmailPostForm, PostForm
from blog.models import Post


class PostListView(ListView):
    queryset = Post.approved.all()
    paginate_by = 5
    context_object_name = "posts"
    template_name = "blog/post/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context, context["object_list"])
        context["new_form"] = PostForm()
        return context


class PostListByUserView(ListView):
    paginate_by = 5
    context_object_name = "posts"
    template_name = "blog/post/list.html"

    def get_queryset(self) -> QuerySet[Any]:
        username = self.kwargs.get("username")
        queryset = Post.objects.filter(author__username=username)

        return queryset


class PostListByTagView(ListView):
    paginate_by = 5
    context_object_name = "posts"
    template_name = "blog/post/list.html"

    def get_queryset(self) -> QuerySet[Any]:
        tag_slug = self.kwargs.get("tag_slug")
        tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = Post.approved.filter(tags__in=[tag])
        return queryset


@require_POST
def post_comment(request, post_id):
    try:
        post = Post.approved.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("No post found")

    comment = None
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = User.objects.get(id=1)
        comment.save()

    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )


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

    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": post.comments.all(), "form": CommentForm()},
    )


def post_share(request, post_id):
    try:
        post = Post.approved.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("No post found")

    if request.method == "GET":
        return render(
            request,
            "blog/post/share.html",
            {"post": post, "form": EmailPostForm(), "sent": False},
        )

    form = EmailPostForm(request.POST)
    sent = False

    if form.is_valid():
        cd = form.cleaned_data
        post_url = request.build_absolute_uri(post.get_absolute_url())
        subject = f"{cd['username']} recommends you read {post.title}"
        message = (
            f"Read {post.title} at {post_url}\n\n"
            f"{cd['username']}'s comments: {cd['comments']}"
        )
        print(subject, message, settings.EMAIL_HOST_USER, [cd["to"]])
        send_mail(subject, message, settings.EMAIL_HOST_USER, [cd["to"]])
        sent = True

    return render(
        request,
        "blog/post/share.html",
        {"post": post, "form": form, "sent": sent},
    )
