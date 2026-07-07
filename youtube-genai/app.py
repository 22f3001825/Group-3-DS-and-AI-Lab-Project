from flask import Flask
from flask_login import LoginManager
from config import Config
import os

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure directories exist
    for d in [Config.TRANSCRIPTS_DIR, Config.PROCESSED_DIR,
              Config.VECTOR_DB_DIR, Config.SESSION_FILE_DIR]:
        os.makedirs(d, exist_ok=True)

    # Flask-Login setup
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in with your IITM email to continue."
    login_manager.login_message_category = "warning"

    # Register blueprints
    from routes.auth      import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.upload    import upload_bp
    from routes.transcript import transcript_bp
    from routes.dataset   import dataset_bp
    from routes.rag       import rag_bp
    from routes.notes     import notes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(transcript_bp)
    app.register_blueprint(dataset_bp)
    app.register_blueprint(rag_bp)
    app.register_blueprint(notes_bp)

    return app

# User loader for Flask-Login
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
