from flask import  Blueprint
from  controladores.ciclista import * 

ciclista = Blueprint('ciclista', __name__)

#Listar
@ciclista.route('/ciclistas',methods = ['GET']) 
def lista_ciclista():
    return get_ciclistas()

#Crear
@ciclista.route('/ciclista',methods = ['POST']) 
def create_ciclista():
    return crear_ciclista()
#devolver 
@ciclista.route('/ciclista/<int:id>',methods = ['GET'])
def devolver_ciclista(id):
    return get_ciclista(id)

#editar contacto 
@ciclista.route('/ciclista/<int:id>', methods =['PUT','PATCH'])
def actualizar_ciclista(id):
    return update_ciclista(id)

#borrar
@ciclista.route('/ciclista/<int:id>', methods =['DELETE'])
def eliminar_ciclista(id):
    return delete_ciclista(id)

#buscar por nombre y apellido 
@ciclista.route('/ciclista/<int:id>', methods =['GET'])
def buscar_NyA(nombre,apellido):
    return buscar_ciclistas(nombre, apellido)

#listar paises en BD
@ciclista.route('/paises', methods =['GET'])
def devolver_paises():
    return get_paises()