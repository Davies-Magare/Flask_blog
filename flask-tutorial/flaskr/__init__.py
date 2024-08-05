import os


from flask import Flask
from .db import db


def create_app(test_config=None):
    #create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY = 'dev',
            SQLALCHEMY_DATABASE_URI='mysql+mysqldb://debian-sys-maint:IRBRRd9IG7Ib3OS0@localhost:3306/flask_blog', #gpt code
        )
    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)

    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #set up SQLAlchemy
    db.init_app(app)    
    
    from .models import User, Post
    #create the tables in the database
    with app.app_context():
        db.create_all()

    #a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello World!'


    from . import auth, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
