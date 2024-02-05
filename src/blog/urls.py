from django.urls import path

from blog.views import post_list

app_name = "blog"

urlpatterns = [
    path("posts/", post_list, name="post_list"),
]
