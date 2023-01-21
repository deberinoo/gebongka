from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

# ----- general routes -----

@views.app_errorhandler(404)
def handle_404(err):
    return render_template("page-not-found.html")

@views.route('/')
def index():
    return render_template("index.html")


@views.route('/features')
def features():
    return render_template("features.html")

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html")