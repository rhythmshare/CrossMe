from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    
    from . import models

    # blueprint
    from .views import main_views, freeboard_views, comment_views, authority_views, menu_views, board_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(board_views.bp)
    app.register_blueprint(freeboard_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(authority_views.bp)
    app.register_blueprint(menu_views.bp)
    
    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime
    
    return app