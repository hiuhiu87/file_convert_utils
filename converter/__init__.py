from flasgger import Swagger
from flask import Flask

from converter.route.converter_controller import converter


def create_app():
    app = Flask(__name__)
    swagger = Swagger(app)
    app.register_blueprint(converter)
    return app
