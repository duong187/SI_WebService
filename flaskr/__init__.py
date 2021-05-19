import os

from flask import Flask
from flask_pymongo import PyMongo

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    app.config["MONGO_URI"] = "mongodb://localhost:27017/data_intergration"
    mongo = PyMongo(app)
    app.db = mongo.db

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #Register blueprint
    from . import auth
    app.register_blueprint(auth.bp)
    from . import fetch
    app.register_blueprint(fetch.bp)
    app.add_url_rule('/', endpoint='index')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # @app.route('/')
    # def home_page():
    #     jobs_info = mongo.db.jobs_info
    #     cur = jobs_info.find({
    #         "address": {"$regex": "Hoàng Quốc Việt+"}
    #     })
    #     job_list = []
    #     for job in cur:
    #         job_list.append(job)
    #     return "\n".join(str(job_list))

    return app