import functools
#from flask import current_app, g
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import InsertOne, DeleteOne, ReplaceOne
from flaskr.db import get_db
from bson.json_util import dumps

bp = Blueprint('fetch', __name__)

@bp.route("/")
def fetch_all():
    db = get_db()
    jobs = db.jobs_info.find()
    jobs = list(jobs)
    return render_template("jobs/index.html", jobs=jobs)

# @bp.route("/fetch_all")
# def fetch_all():
#     db = get_db()
#     jobs = db.jobs_info.find()
#     data = dumps(list(jobs))
#     return data