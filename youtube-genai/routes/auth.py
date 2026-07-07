from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from config import Config
from models import User

auth_bp = Blueprint("auth", __name__)


def is_valid_iitm_email(email: str) -> bool:
    """Allow only emails ending with allowed IITM domains."""
    email = email.strip().lower()
    return any(email.endswith(f"@{domain}") for domain in Config.ALLOWED_EMAIL_DOMAINS)


@auth_bp.route("/", methods=["GET"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    from flask_login import current_user
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template("login.html")

        if not is_valid_iitm_email(email):
            flash("Only IIT Madras institutional emails are allowed (e.g. 22f1000559@ds.study.iitm.ac.in).", "danger")
            return render_template("login.html")

        # Mock auth — any non-empty password accepted
        user = User.login(email)
        login_user(user)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("dashboard.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
