import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ['FLASK_SECRET_KEY'],
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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

    from . import db
    db.init_app(app)


    # SETTING UP HOMEPAGE

    homepage = 'upload.single_file'

    app.add_url_rule('/', endpoint=homepage)

    @app.route('/home')
    def index():
        from flask import redirect, url_for
        return redirect(url_for(homepage))


    # REGISTERING BLUEPRINTS

    from . blueprints import upload
    app.register_blueprint(upload.bp)

    from . blueprints import process
    app.register_blueprint(process.bp)

    return app


def get_domain():
    from flask import request
    domain = request.root_url[:-1]
    return domain
