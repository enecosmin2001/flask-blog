from sqlalchemy.sql.expression import func

from app import db
from app.models import Post


class Dreamer:
    @staticmethod
    def _dream(text_to_img):
        return f"test-bytes : {text_to_img}"

    @staticmethod
    def save_image(post_id, img_bytes):
        return f"/path/at/{post_id}/{img_bytes}"

    @classmethod
    def generate_dream_image(cls, post_id, dream_text):
        image_bytes = Dreamer._dream(dream_text)
        post = Post.query.get(post_id)
        post.image_path = Dreamer.save_image(post.id, image_bytes)

        db.session.add(post)
        db.session.commit()

        return post.image_path

    @classmethod
    def generate_missing_dream_images(cls):
        for p in Post.query.filter(
            Post.image_path == None, func.length(Post.text_to_image) > 0
        ).all():
            cls.generate_dream_image(p.id, p.text_to_image)
