from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from blog.managers import PublishedManager


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100, unique_for_date="published")
    body = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    approved = PublishedManager()

    class Meta:
        ordering = ["-published"]
        indexes = [models.Index(fields=["-published"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[
                self.published.year,
                self.published.month,
                self.published.day,
                self.slug,
            ],
        )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    body = models.TextField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created"])]

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
