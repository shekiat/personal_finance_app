from flask import Flask

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__)
    app.secret_key="secret_key"

    from . import run_website
    app.register_blueprint(run_website.bp)

    from . import db
    db.init_app(app)

    return app