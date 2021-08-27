from flask import Flask, render_template, make_response, request
from flask.config import Config
from flask_restful import Api, Resource
import logging as logger

from functools import wraps

import config

# Wrapper documentation
# https://flask-restful.readthedocs.io/en/latest/extending.html

#Setup Logger configuration
logger.basicConfig(format=config.FORMAT, level=logger.DEBUG)
logger.info("Start running")

def add_title(func):
    @wraps(func)
    def wrapper():
        ret_val_dict = {
            "title": "Rajesh is AWESOME !", 
            "header":"Is there anything Rajesh cant do ?",
            "back_url" : "<a href='/api/v1/get_rajesh_secret_identity'> Get back to awesome home page </a>"
            }

        return func(ret_val_dict)

    return wrapper

class Resource(Resource):
    method_decorators = [add_title]   # applies to all inherited resources

class greet_and_bless(Resource):
    def get(self,*args):
        return make_response(render_template('home_page.html',back_url=args[0]['back_url']))

class get_rajesh_secret_identity(Resource):
    def get(self,*args):
        logger.info(*args)
        return make_response(render_template('get_password.html',title=args[0]['title'],header=args[0]['header']))

    def post(self,*args):
        logger.info(*args)
        if request.form['password'] == config.PASSWORD :
            show_template = 'rajesh_secret_identity.html'
        else:
            show_template = 'incorrect_password.html'

        # return make_response(render_template('show_password.html', form_data = CORRECT_PASSWORD))
        return make_response(render_template(show_template,title=args[0]['title'],header=args[0]['header'],back_url=args[0]['back_url']))

try : 
    # EB looks for an 'application' callable by default.
    application = Flask(__name__)
    api = Api(application, prefix="/api/v1/")

    api.add_resource(greet_and_bless,'/')
    api.add_resource(get_rajesh_secret_identity,"/get_rajesh_secret_identity")
except Exception as error:
    logger.exception(error)

@application.errorhandler(404)
def page_not_found(e):
    return make_response(render_template('404_error.html')), 404


if __name__ == "__main__":
    try :
        application.debug = True
        application.run()
    except Exception as error:
        logger.exception(error)