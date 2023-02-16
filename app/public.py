from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.crud import crud_url
from app.db import get_db
from app.utils import check_url

bp = Blueprint("public", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    url_shortened = None
    url = None
    if request.method == "POST":
        url, err = request.form.get("url"), None
        if not url:
            err = "It is necessary to enter a url"
        elif len(url) > 1028:
            err = "Maximum url length is 1028"
        elif not check_url(url):
            err = "Not a valid url"
        else:
            db = get_db()
            url_shortened = crud_url.create(db, url)
        if err:
            flash(err)
    return render_template("index.html", url_shortened=url_shortened, original_url=url)


@bp.route("/<string:url>")
def redirect_url(url):
    db = get_db()
    original_url = crud_url.read(db, f"{current_app.config['CURRENT_HOST']}/{url}")
    if original_url:
        return redirect(original_url)
    return redirect(url_for(".index"))
