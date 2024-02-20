from datetime import datetime

from ninja import Router, Schema

from blog.models import Post

router = Router()


class PostIn(Schema):
    title: str
    slug: str
    body: str


class PostOut(Schema):
    title: str
    slug: str
    body: str
    created: datetime


@router.get("/", response=list[PostOut])
def post_list(request):
    return Post.approved.all()


@router.get("/{post_id}", response=PostOut)
def post_detail(request, post_id: int):
    return Post.objects.get(id=post_id)


@router.post("/")
def post_create(request, payload: PostIn):
    values = payload.dict()
    # values["user"] = request.user
    post = Post.objects.create(**values)
    return {"id": post.id}
