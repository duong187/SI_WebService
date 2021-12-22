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
    #cities = ['ha hoi', 'thanh pho ho chi minh', 'da nang']
    db = get_db()
    jobs_count = db.jobs_info.count()
    cities = db.jobs_info.distinct('city')
    city_job_data = []
    c = []
    num = []
    salary = []
    for city in cities:
        query = {"city": city}
        # print(city + '-' + str(db.jobs_info.find(query).count()/jobs_count))
        # if(db.jobs_info.find(query).count()/jobs_count > 0.05):
        city_job_data.append({
            'city': city,
            'num': db.jobs_info.find(query).count(),
        })
    for job in db.jobs_info.find():
        if (int(job["salary"]) != 0):
            salary.append(int(job["salary"])/1000000)
            # print(job["maxSalary"])
    sorted_data = sorted(city_job_data, key=lambda k: k['num'], reverse=True)
    for i in range(5):
        c.append(sorted_data[i]['city'])
        num.append(sorted_data[i]['num'])
    # Draw Chart
    # print(city_jobs_count)
    fig = Figure()
    gs = fig.add_gridspec(1, 1)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_title("5 tỉnh thành có số lương công việc nhiều nhất")
    # ax2 = fig.add_subplot(gs[1, 0])
    # ax3 = fig.add_subplot(gs[0, 1])
    # ax4 = fig.add_subplot(gs[1, 1])
    pie = ax1.pie(num, autopct='%1.3f%%')
    ax1.legend(pie[0], c, loc="lower right", bbox_to_anchor=(0.25, 0))
    # ax2.pie(city_jobs_count, labels = cities,autopct='%1.2f%%')
    # ax3.pie(city_jobs_count, labels = cities,autopct='%1.2f%%')
    # ax4.pie(city_jobs_count, labels = cities,autopct='%1.2f%%')
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # return f"<img src='data:image/png;base64,{data}'/>"
    fig2 = Figure()
    gs2 = fig2.add_gridspec(1, 1)
    ax2 = fig2.add_subplot(gs[0, 0])
    ax2.set_xlabel('Mức lương (triệu đồng)')
    ax2.set_ylabel('Số lượng công việc')
    ax2.set_title('Phân bố mức lương')
    # ax2 =fig2.add_subplot(gs[1, 0])
    # ax3 = fig2.add_subplot(gs[0, 1])
    # ax4 = fig2.add_subplot(gs[1, 1])
    hist = ax2.hist(salary, 80)
    # ax2.pie(city_jobs_count, labels = cities,autopct='%1.2f%%')
    # ax3.pie(city_jobs_count, labels = cities,autopct='%1.2f%%')
    # ax4.pie(city_jobs_count, labels = cities,autopct='%1.2f%%')
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig2.savefig(buf, format="png")
    # Embed the result in the html output.
    data2 = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template("charts/pie.html", pie=data, hist=data2)
