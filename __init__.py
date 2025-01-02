import os

from flask import Flask

print("DATABASE_HOST:", os.environ.get('FLASK_DATABASE_HOST'))
print("DATABASE_USER:", os.environ.get('FLASK_DATABASE_USER'))
print("DATABASE_PASSWORD:", os.environ.get('FLASK_DATABASE_PASSWORD'))
print("DATABASE:", os.environ.get('FLASK_DATABASE'))

def create_app():
    app = Flask(__name__)
    

    app.config.from_mapping(
        SECRET_KEY =  'mikey',
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE'),
    )
    
    
    
    from . import db
    
    db.init_app(app)
    
    from . import auth
    from . import todo
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)
    @app.route('/home')
    def home():
        return 'hola'
    
    return app