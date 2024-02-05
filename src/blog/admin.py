from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "author",
        "status",
        "published",
        "updated",
    ]
    list_filter = ["author", "status", "updated"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published"
    ordering = ["status", "published", "created", "title", "author"]
