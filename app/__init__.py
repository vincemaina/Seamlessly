import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template

from . config import file_limit_megabytes

def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # configuring app settings
    app.config.from_mapping(
        SECRET_KEY=os.environ['FLASK_SECRET_KEY'],
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        MAX_CONTENT_LENGTH=file_limit_megabytes*1024*1024,
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


    # INITIALISE DATABASE
    from . import db
    db.init_app(app)


    # SETTING UP HOMEPAGE

    homepage = 'upload.single_file'

    app.add_url_rule('/', endpoint=homepage, methods=['GET', 'POST'])

    @app.route('/home', methods=['GET', 'POST'])
    def index():
        from flask import redirect, url_for
        return redirect(url_for(homepage))


    # SETTING UP OTHER ROUTES

    @app.route('/help')
    def guide():
        
        from flask import flash, redirect, url_for

        flash('This page has not yet been added.')

        return redirect('https://github.com/vchapandrews/seamlessly')


    # HANDLING ERROR PAGES

    from . error_handling import request_entity_is_too_large
    app.register_error_handler(413, request_entity_is_too_large)

    from . error_handling import page_not_found
    app.register_error_handler(404, page_not_found)


    # REGISTERING BLUEPRINTS

    from . blueprints import upload
    app.register_blueprint(upload.bp)

    from . blueprints import process
    app.register_blueprint(process.bp)

    from . blueprints import admin
    app.register_blueprint(admin.bp)

    from . blueprints import configure_css_background
    app.register_blueprint(configure_css_background.bp)

    return app


def get_domain():
    from flask import request
    domain = request.root_url[:-1]
    return domain
