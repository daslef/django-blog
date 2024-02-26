from datetime import datetime

from django.utils.text import slugify
from ninja import Router, Schema

from blog.models import Comment, Post

router = Router()


class PostIn(Schema):
    title: str
    body: str


class PostOut(Schema):
    title: str
    slug: str
    body: str
    created: datetime


class CommentIn(Schema):
    post_id: int
    body: str


class CommentOut(Schema):
    post_id: int
    user_id: int
    body: str
    created: datetime


@router.get("/comments/{post_id}", response=list[CommentOut])
def comment_list(request, post_id: int):
    post = Post.objects.get(id=post_id)
    return post.comments


@router.post("/comments/", response=CommentOut)
def comment_create(request, payload: CommentIn):
    values = payload.dict()
    values["user_id"] = int(request.user.id)
    comment = Comment.objects.create(**values)
    comment.save()
    return comment


@router.get("/", response=list[PostOut])
def post_list(request):
    return Post.approved.all()


@router.get("/{post_id}", response=PostOut)
def post_detail(request, post_id: int):
    return Post.objects.get(id=post_id)


@router.post("/")
def post_create(request, payload: PostIn):
    values = payload.dict()
    values["author_id"] = int(request.user.id)
    values["slug"] = slugify(values["title"])
    post = Post.objects.create(**values)
    post.save()
    return {"id": post.id}
