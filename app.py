from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    register_routes(app)
    # 自动 reload jinja
    app.jinja_env.auto_reload = True
    return app


def register_routes(app):
    # 注册蓝图
    # 有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀
    from routes.board import main as board_routes
    from routes.index import main as index_routes
    from routes.mail import main as mail_routes
    from routes.reply import main as reply_routes
    from routes.topic import main as topic_routes
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(mail_routes, url_prefix='/mail')
    return app


if __name__ == '__main__':
    app = create_app('development')
    cfg = dict(
        host='localhost',
        port=4000,
        threaded=True,
    )
    app.run(**cfg)
