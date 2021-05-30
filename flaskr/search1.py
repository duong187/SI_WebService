from flaskr.search.index import Index
from flaskr.search.timing import timing
import requests
import os.path
from flaskr.search.documents import Abstract
import time
from lxml import etree
import gzip
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
import json
from bson.json_util import dumps

bp = Blueprint('search1', __name__, url_prefix='/s')


def load_documents():
    start = time.time()
    db = get_db()
    jobs = db.jobs_info.find()
    jobs = list(jobs)
    for job in jobs:
        doc_id = 0
        job = json.load(job)
        title = job['cleanTitle']
        url = job['url']
        address = job['address']
        company = job['company']
        salary = job['salary']
        yield Abstract(ID=doc_id, title=title, url=url, address=address, company=company, salary=salary)
        doc_id += 1

    end = time.time()
    print(f'Parsing XML took {end - start} seconds')


def index_documents(documents, index):
    for i, document in enumerate(documents):
        index.index_document(document)
        if i % 5000 == 0:
            print(f'Indexed {i} documents', end='\r')
    return index


@bp.route("/")
def index():
    return render_template("jobs/index.html")
