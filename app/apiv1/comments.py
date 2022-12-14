from flask import current_app, g, jsonify, request, url_for

from .. import db
from ..models import Comment, Permission, Post
from . import apiv1
from .decorators import permission_required


@apiv1.route("/comments/")
def get_comments():
    page = request.args.get("page", 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page,
        per_page=current_app.config["FLASKBLOG_COMMENTS_PER_PAGE"],
        error_out=False,
    )
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("apiv1.get_comments", page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for("apiv1.get_comments", page=page + 1)
    return jsonify(
        {
            "comments": [comment.to_json() for comment in comments],
            "prev": prev,
            "next": next,
            "count": pagination.total,
        }
    )


@apiv1.route("/comments/<int:id>")
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())


@apiv1.route("/posts/<int:id>/comments/")
def get_post_comments(id):
    post = Post.query.get_or_404(id)
    page = request.args.get("page", 1, type=int)
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page,
        per_page=current_app.config["FLASKBLOG_COMMENTS_PER_PAGE"],
        error_out=False,
    )
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for("apiv1.get_post_comments", id=id, page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for("apiv1.get_post_comments", id=id, page=page + 1)
    return jsonify(
        {
            "comments": [comment.to_json() for comment in comments],
            "prev": prev,
            "next": next,
            "count": pagination.total,
        }
    )


@apiv1.route("/posts/<int:id>/comments/", methods=["POST"])
@permission_required(Permission.COMMENT)
def new_post_comment(id):
    post = Post.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    comment.post = post
    db.session.add(comment)
    db.session.commit()
    return (
        jsonify(comment.to_json()),
        201,
        {"Location": url_for("apiv1.get_comment", id=comment.id)},
    )
