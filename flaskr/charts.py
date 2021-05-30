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

@bp.route('/pie_city')
def pie_city():
    cities = ['Ha Noi', 'Ho Chi Minh', 'Danang']
    db = get_db()
    city_jobs_count = []
    for city in cities:
        query = {"city":city}
        city_jobs_count.append(db.itviec.find(query).count())
    #Draw Chart
    fig = Figure()
    gs = fig.add_gridspec(2, 2)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[0, 1])
    ax4 = fig.add_subplot(gs[1, 1])
    ax1.pie(city_jobs_count, labels = cities,autopct='%1.2f%%')
    ax2.pie(city_jobs_count, labels = cities,autopct='%1.2f%%')
    ax3.pie(city_jobs_count, labels = cities,autopct='%1.2f%%')
    ax4.pie(city_jobs_count, labels = cities,autopct='%1.2f%%')
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    #return f"<img src='data:image/png;base64,{data}'/>"
    return render_template("charts/pie.html", pie=data)