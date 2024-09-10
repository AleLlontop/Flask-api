from flask import Flask, render_template
from extension import db  # Importa la instancia de db
from model.db_models import *  


def create_app():
    app = Flask(__name__)

    # Configura la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ciclismo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa la app con SQLAlchemy
    db.init_app(app)
    
    # Registrar Blueprints
    from rutas.ciclista import ciclista
    app.register_blueprint(ciclista)
    
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    
    
@app.route("/")
def hello_world():
    return render_template ('index.html')


