from flask import Flask

def create_app():
    app = Flask(__name__)
    from .app import webhook
    app.register_blueprint(webhook)
    return app