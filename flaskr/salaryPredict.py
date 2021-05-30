import functools
#from flask import current_app, g
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import InsertOne, DeleteOne, ReplaceOne

from flaskr.db import get_db
from flaskr.auth import login_required

import sys
import os
import pandas as pd
#from . import features
from .features import *
from . import features

import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

sys.modules['features'] = features

# class FeatureMapper:
#     def __init__(self, features):
#         self.features = features

#     def fit(self, X, y=None):
#         for feature_name, column_name, extractor in self.features:
#             extractor.fit(X[column_name], y)

#     def transform(self, X):
#         extracted = []
#         for feature_name, column_name, extractor in self.features:
#             fea = extractor.transform(X[column_name])
#             if hasattr(fea, "toarray"):
#                 extracted.append(fea.toarray())
#             else:
#                 extracted.append(fea)
#         if len(extracted) > 1:
#             return np.concatenate(extracted, axis=1)
#         else: 
#             return extracted[0]

#     def fit_transform(self, X, y=None):
#         extracted = []
#         for feature_name, column_name, extractor in self.features:
#             fea = extractor.fit_transform(X[column_name], y)
#             if hasattr(fea, "toarray"):
#                 extracted.append(fea.toarray())
#             else:
#                 extracted.append(fea)
#         if len(extracted) > 1:
#             return np.concatenate(extracted, axis=1)
#         else: 
#             return extracted[0]

# def feature_extractor():
#     features = [('description-Bag of Words', 'description', CountVectorizer(max_features=100)),
#                 ('title-Bag of Words', 'title', CountVectorizer(max_features=100)),
#                 ('address-Bag of Words', 'address', CountVectorizer(max_features=100)),
#                 ('benefits-Bag of Words', 'benefits', CountVectorizer(max_features=100)),
#                 ('company-Bag of Words', 'company', CountVectorizer(max_features=100)),
#                 ('city-Bag of Words', 'city', CountVectorizer(max_features=100))]
#     combined = FeatureMapper(features)
#     return combined

# def get_pipeline():
#     features = feature_extractor()
#     steps = [("extract_features", features),
#              ("classify", RandomForestRegressor(n_estimators=50, 
#                                                 verbose=2,
#                                                 n_jobs=1,
#                                                 min_samples_split=30,
#                                                 random_state=3465343))]
#     return Pipeline(steps)

#features = feature_extractor()

def load_model():
    #path = "salary_prediction_itviec.pickle"
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'salary_prediction_itviec.pickle')
    return pickle.load(open(path, "rb"))

def identity(x):
    return x

bp = Blueprint('salaryPredict', __name__, url_prefix='/salarypredict')

@bp.route('/pred', methods=('GET', 'POST'))
def index():
    prediction='Hãy nhập dữ liệu'
    if request.method == 'POST':
        dict = {}
        dict["address"] = [identity(request.form["address"])]
        dict["benefits"] = [identity(request.form["benefits"])]
        dict["company"] = [identity(request.form["company"])]
        dict["description"] = [identity(request.form["description"])]
        dict["title"] = [identity(request.form["title"])]
        dict["city"] = [identity(request.form["city"])]
        dict["cleanTitle"] = [identity(request.form["cleanTitle"])]
        valid = pd.DataFrame.from_dict(dict)
        #Load Model
        classifier = load_model()
        prediction = classifier.predict(valid)   
        prediction = prediction.reshape(len(prediction), 1)
        prediction = prediction.flatten()[0]
    return render_template('salary/predict_form.html', prediction = prediction)



