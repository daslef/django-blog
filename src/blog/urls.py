from django.urls import path

from blog.views import PostListView, post_comment, post_detail, post_share

app_name = "blog"

urlpatterns = [
    path(
        "posts/<int:year>/<int:month>/<int:day>/<slug:slug>",
        post_detail,
        name="post_detail",
    ),
    path("posts/<int:post_id>/comment/", post_comment, name="post_comment"),
    path("posts/<int:post_id>/share/", post_share, name="post_share"),
    path("posts/", PostListView.as_view(), name="post_list"),
]
