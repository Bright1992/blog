from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import re
from flask.ext.mail import Mail

app=Flask(__name__)
app.config.from_object('config')
################mail setting#####
mail=Mail(app)
######sql initialize#############
db=SQLAlchemy(app)
#############login manager######
lm=LoginManager()
lm.init_app(app)
lm.login_view='login'
################error############
import errorlog
errorlog.ErrorMail()
#####blueprint registe###########
from flaskr.postsviews import viewposts
app.register_blueprint(viewposts)
##################################
re_email_str=re.compile(r'([0-9a-zA-Z][0-9a-zA-Z._]{,15}[0-9a-zA-Z])@([0-9a-zA-Z.]+)$')
re_password_str=re.compile(r'\w{6,16}')
re_uppercase=re.compile(r'[A-Z]+')
re_number=re.compile(r'[0-9]+')
###################import py pacage member
import appviews,forms,models,postsviews


