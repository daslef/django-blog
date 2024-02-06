from django.urls import path

from blog.views import post_detail, post_list

app_name = "blog"

urlpatterns = [
    path("posts/<int:id>", post_detail, name="post_detail"),
    path("posts/", post_list, name="post_list"),
]
