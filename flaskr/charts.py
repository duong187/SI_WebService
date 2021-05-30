from math import ceil
import functools
#from flask import current_app, g
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import InsertOne, DeleteOne, ReplaceOne

from flaskr.db import get_db
from flaskr.auth import login_required

from bson.json_util import dumps

# for matplotlib visualization
import base64
from io import BytesIO
from matplotlib.figure import Figure

bp = Blueprint('charts', __name__, url_prefix='/charts')


@bp.route("/chart_types")
def chart_types():
    return render_template("charts/chart_types.html")


@bp.route("/pie")
def pie():
    fig = Figure()
    # axes = fig.subplots()
    langs = ['C', 'C++', 'Java', 'Python', 'PHP']
    students = [23, 17, 35, 29, 12]
    # axes.pie(students, labels = langs,autopct='%1.2f%%')

    gs = fig.add_gridspec(1, 1)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.pie(students, labels=langs, autopct='%1.2f%%')

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # return f"<img src='data:image/png;base64,{data}'/>"
    return render_template("charts/pie.html", pie=data)
