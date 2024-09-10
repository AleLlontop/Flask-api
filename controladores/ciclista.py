from datetime import datetime
from flask import  request, jsonify
from model.db_models import Ciclista,Pais, db 
from sqlalchemy import and_

#Listar 
def get_ciclistas():
    ciclistas = Ciclista.query.all()
    return jsonify({'ciclistas': [ciclista.serialize() for ciclista in ciclistas]})

#Crear 
def crear_ciclista():
    data = request.get_json()

    # Convertir edad a entero
    edad = int(data['edad'])
    # Buscar si el país ya existe
    pais = Pais.query.filter_by(descripcion=data['pais']).first()
    
    # Convertir la fecha de nacimiento
    fecha_nacimiento = datetime.strptime(data['fechaNacimiento'], '%Y-%m-%d').date()

    # Si no existe, crearlo
    if not pais:
        pais = Pais(descripcion=data['pais'])
        db.session.add(pais)
        db.session.commit()  # Guardamos el país en la base de datos para obtener su id

    # Crear una nueva instancia de Ciclista
    ciclista = Ciclista(
        nombre=data['nombre'],
        apellido=data['apellido'],
        edad=edad,
        fechaNacimiento=fecha_nacimiento,
        pais=pais  
    )

    # Agregar y guardar el ciclista en la base de datos
    db.session.add(ciclista)
    db.session.commit()

    return jsonify(ciclista.serialize()), 201

#devolver un ciclista
def get_ciclista(id) :
    ciclista = Ciclista.query.get(id)
    if not  ciclista:
        return jsonify({'message':'Ciclista No encontrado'}), 404 
    return jsonify( ciclista.serialize())


#buscar por nombre y apellido 
def buscar_ciclistas(nombre, apellido):
    ciclistas = Ciclista.query.filter(and_(Ciclista.nombre == nombre, Ciclista.apellido == apellido)).all()
    if not ciclistas:
        return jsonify({'message': 'No se encontraron ciclistas con ese nombre y apellido'}), 404
    return jsonify([ciclista.serialize() for ciclista in ciclistas])

#devolver paisese cargados en la BD
def get_paises() :
    paises = Pais.query.all()
    return jsonify({'paises': [pais.serialize() for pais in paises]})


def update_ciclista(id):    
     
     ciclista = Ciclista.query.get_or_404(id)
     
     data = request.get_json()
     
     if 'nombre' in data: 
         ciclista.name= data ['nombre']
     if 'apellido' in data:
         ciclista.apellido = data ['apellido'] 
     if 'edad' in data:
        try:
            ciclista.edad = int(data['edad'])
        except ValueError:
            return jsonify({"error": "La edad debe ser un número entero válido"}), 400
     if 'fechaNacimiento' in data:
        try:
            fecha_nacimiento = datetime.strptime(data['fechaNacimiento'], '%Y-%m-%d').date()
            ciclista.fechaNacimiento = fecha_nacimiento
        except ValueError:
            return jsonify({"error": "La fecha debe estar en el formato YYYY-MM-DD"}), 400

     if 'pais' in data:
        
        pais = Pais.query.filter_by(descripcion=data['pais']).first()
        
        # Si no existe, creo un nuevo país
        if not pais:
            pais = Pais(descripcion=data['pais'])
            db.session.add(pais)
            db.session.commit()  #guardamos
            
        ciclista.pais = pais     # Asignamos  
        
       
     db.session.commit()
      
     return jsonify({'message':'Ciclista actualizado  con exito',
                    'contact': ciclista.serialize()
    })
    
#delete 
def delete_ciclista(id):
    ciclista = Ciclista.query.get(id)
    
    if not ciclista:
        return jsonify({'message': 'Ciclista No encontrado'}), 404
    
    # Desvincular la relación con pais
    ciclista.pais_id = None
    db.session.commit()
    
    # Eliminar ciclista
    db.session.delete(ciclista)
    db.session.commit()
    
    return jsonify({'message': 'Ciclista eliminado correctamente'})
