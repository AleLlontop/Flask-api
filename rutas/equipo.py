from flask import  Blueprint
from flask import  request, jsonify
from datetime import datetime
from model.db_models import *

#Crear equipo
equipo = Blueprint('equipo', __name__)

@equipo.route('/equipo',methods = ['POST']) 
def create_equipo():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos no enviados correctamente.'}), 400

    # Obtener datos del cuerpo de la solicitud

    nombre_equipo = data.get('nombre')
    pais = data.get('pais')
    director_id = data.get('director')
    contratos = data.get('contratos', [])
    
    print(data)

    if not (pais,director_id , nombre_equipo  and contratos ):
        return jsonify({'error': 'Todos los campos son obligatorios: '}), 400

    equipo = Equipo(nombre=nombre_equipo, pais_id=pais, director_id=director_id)
    db.session.add(equipo)
    db.session.commit()
    print(f"ID del equipo asignado: {equipo.id}")
    
    # Crear el contrato
    for contrato_data in contratos:
        fecha_inicio = contrato_data.get('fecha_inicio')
        fecha_fin = contrato_data.get('fecha_fin')
        ciclista_id = contrato_data.get('ciclista')
        
        # Convertir a objetos de tipo date
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

        contrato = Contrato(
            equipo_id=equipo.id,
            ciclista_id=ciclista_id,
            fechaInicio =fecha_inicio,
            fechaFin=fecha_fin,
        )
        db.session.add(contrato)

    db.session.commit()
    return jsonify({'message': 'Equipo y contratos creados correctamente'})  


