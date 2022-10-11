from flask import current_app, jsonify, request, url_for

from ..models import Post, User
from . import apiv1


@apiv1.route("/users/<int:id>")
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@apiv1.route("/users/<int:id>/posts/")
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get("page", 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config["FLASKBLOG_POSTS_PER_PAGE"], error_out=False
    )
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("apiv1.get_user_posts", id=id, page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for("apiv1.get_user_posts", id=id, page=page + 1)
    return jsonify(
        {
            "posts": [post.to_json() for post in posts],
            "prev": prev,
            "next": next,
            "count": pagination.total,
        }
    )


@apiv1.route("/users/<int:id>/timeline/")
def get_user_followed_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get("page", 1, type=int)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config["FLASKBLOG_POSTS_PER_PAGE"], error_out=False
    )
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("apiv1.get_user_followed_posts", id=id, page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for("apiv1.get_user_followed_posts", id=id, page=page + 1)
    return jsonify(
        {
            "posts": [post.to_json() for post in posts],
            "prev": prev,
            "next": next,
            "count": pagination.total,
        }
    )
