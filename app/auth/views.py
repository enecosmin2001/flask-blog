from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .. import db
from ..email import send_email
from ..models import User
from . import auth
from .forms import LoginForm, UserRegistrationForm


@auth.before_app_request
def before_request():
    if (
        current_user.is_authenticated
        and not current_user.confirmed
        and request.blueprint != "auth"
        and request.blueprint != "static"
    ):
        return redirect(url_for("auth.unconfirmed"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()

        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)

            next_url = url_for("main.index")
            if request.args.get("next"):
                next = request.args.get("next")
                if not next.startswith("/"):
                    next_url = next

            return redirect(next_url)

        flash("Invalid username or password!")
    return render_template("auth/login.html", form=login_form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    register_form = UserRegistrationForm()
    if register_form.validate_on_submit():
        user = User(
            email=register_form.email.data,
            username=register_form.username.data,
            password=register_form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(
            user.email,
            "Confirm your account",
            "auth/email/confirm",
            user=user,
            token=token,
        )
        flash("A confirmation email has been sent to your email.")
        return redirect(url_for("main.index"))
    return render_template("auth/register.html", form=register_form)


@auth.route("/unconfirmed")
@login_required
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        db.session.commit()
        flash("You have confirmed your account. Welcome!")
    else:
        flash("The confirmation link is invalid or has expired.")
    return redirect(url_for("main.index"))


@auth.route("/resend_confirmation")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(
        current_user.email,
        "Confirm your account",
        "auth/email/confirm",
        user=current_user,
        token=token,
    )
    flash("A new confirmation link has been sent to your email.")
    return redirect(url_for("main.index"))
