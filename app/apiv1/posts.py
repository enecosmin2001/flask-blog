from flask import g, jsonify, request, url_for

from app import db
from app.models import Permission, Post

from ..decorators import permission_required
from . import apiv1
from .errors import forbidden


@apiv1.route("/posts/", methods=["POST"])
@permission_required(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(
        post.to_json(), 201, {"Location": url_for("apiv1.get_post", id=post.id)}
    )


@apiv1.route("/posts/<int:id>", methods=["PUT"])
@permission_required(Permission.WRITE)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and not g.current_user.can(Permission.ADMIN):
        return forbidden("Insufficient permissions")
    post.body = request.json.get("body", post.body)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())


@apiv1.route("/posts/")
def get_posts():
    posts = Post.query.all()
    return jsonify({"posts": [post.to_json() for post in posts]})


@apiv1.route("/posts/<int:id>")
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())
