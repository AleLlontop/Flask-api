from flask import Flask, render_template
from extension import db  # Importa la instancia de db
from model.db_models import *  
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    #  habilita CORS para todos los orígenes
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Configura la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ciclismo.db?timeout=20'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa la app con SQLAlchemy
    db.init_app(app)
    
    # Registrar Blueprints
    from rutas.ciclista import ciclista
    app.register_blueprint(ciclista)
    from rutas.equipo import equipo
    app.register_blueprint(equipo)
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    


