from flask import Blueprint

apiv1 = Blueprint("apiv1", __name__)

from . import authentication, comments, errors, posts, users
