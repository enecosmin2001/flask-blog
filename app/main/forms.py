from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError

from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class EditProfileForm(FlaskForm):
    name = StringField("Real Name", validators=[Length(0, 64)])
    location = StringField("Location", validators=[Length(0, 64)])
    about_me = TextAreaField("About Me")
    submit = SubmitField("Save")


class EditProfileAdminForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Username must only have dots, letters, numbers or underscores.",
            ),
        ],
    )
    confirmed = BooleanField("Confirmed")
    role = SelectField("Role", coerce=int)
    name = StringField("Real Name", validators=[Length(0, 64)])
    location = StringField("Location", validators=[Length(0, 64)])
    about_me = TextAreaField("About Me")
    submit = SubmitField("Save")

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [
            (role.id, role.name) for role in Role.query.order_by(Role.name).all()
        ]
        self.user = user

    def validate_email(self, field):
        if (
            field.data != self.user.email
            and User.query.filter_by(email=field.data).first()
        ):
            raise ValidationError("Email already registered.")

    def validate_username(self, field):
        if (
            field.data != self.user.username
            and User.query.filter_by(username=field.data).first()
        ):
            raise ValidationError("Username already in use.")


class PostForm(FlaskForm):
    body = PageDownField("What do you dream about?", validators=[DataRequired()])
    text_to_img = StringField("Text to image", validators=[Length(1, 100)])
    submit = SubmitField("Post")


class CommentForm(FlaskForm):
    body = PageDownField("", validators=[DataRequired()])
    submit = SubmitField("Submit")
