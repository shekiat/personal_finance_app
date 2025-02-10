from flask import Flask

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__)
    app.secret_key="secret_key"

    from . import home
    app.register_blueprint(home.bp)

    from . import dashboard
    app.register_blueprint(dashboard.bp)

    from . import db
    db.init_app(app)

    return app