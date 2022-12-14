import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "APP.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello

    from .db import db

    with app.app_context():
        db.init_db()
    db.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import api

    app.register_blueprint(api.api)

    from . import routes

    with app.app_context():
        routes.init_routes(app)

    return app


if __name__ == "__main__":
    create_app()
