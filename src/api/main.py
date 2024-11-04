from flask import Flask
from src.api.user_controller import user_controller

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua_chave_secreta'

    # Registrar o blueprint
    app.register_blueprint(user_controller, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
