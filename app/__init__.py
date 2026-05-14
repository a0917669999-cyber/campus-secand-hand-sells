import os
import sqlite3
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    app.config['DATABASE'] = os.path.join(app.instance_path, 'database.db')

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize database
    def init_db():
        with app.app_context():
            db = sqlite3.connect(app.config['DATABASE'])
            with app.open_resource('../database/schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
    
    # Expose init_db command to CLI
    import click
    @app.cli.command('init-db')
    def init_db_command():
        """Clear the existing data and create new tables."""
        init_db()
        click.echo('Initialized the database.')

    # If database file doesn't exist, create tables automatically
    if not os.path.exists(app.config['DATABASE']):
        init_db()

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.items import items_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(api_bp)

    return app
