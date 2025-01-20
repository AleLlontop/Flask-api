
from extension import db

# Modelo para la tabla Pais
class Pais(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(45), nullable=False) #no acepta valores nulos 

    def serialize(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion
        }

# Modelo para la tabla Ciclista
class Ciclista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    apellido = db.Column(db.String(45), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    fechaNacimiento = db.Column(db.Date, nullable=False)
    pais_id = db.Column(db.Integer, db.ForeignKey('pais.id'), nullable=True)
    pais = db.relationship('Pais', backref='ciclistas') # desde el objeto Pais accedo a todos los ciclistas asociados a ese país.
    #pais.ciclistas

    def serialize(self):     #Recupera Atributos
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'fechaNacimiento': self.fechaNacimiento.strftime('%Y-%m-%d'),
            'pais': self.pais.descripcion
        }

# Modelo para la tabla Equipo
class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    pais_id = db.Column(db.Integer, db.ForeignKey('pais.id'), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'), nullable=False)

    pais = db.relationship('Pais', backref='equipos')
    director = db.relationship('Director', backref='equipos')
    contratos = db.relationship('Contrato', backref='equipo', lazy=True) #new

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'pais': self.pais.serialize(),
            'director': self.director.serialize(),
            'contratos': [contrato.serialize() for contrato in self.contratos],
            'ciclistas': [contrato.ciclista.serialize() for contrato in self.contratos]  # Extrae ciclistas desde los contratos
        }

# Modelo para la tabla Director
class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    apellido = db.Column(db.String(45), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido
        }

# Modelo para la tabla Contrato
class Contrato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    ciclista_id = db.Column(db.Integer, db.ForeignKey('ciclista.id'), nullable=False)
    fechaInicio = db.Column(db.Date, nullable=False)
    fechaFin = db.Column(db.Date, nullable=False)


    #equipo = db.relationship('Equipo', backref='contratos')
    ciclista = db.relationship('Ciclista', backref='contratos')

    def serialize(self):
        return {
            'id': self.id,
            'fechaInicio': self.fechaInicio.strftime('%Y-%m-%d'),
            'fechaFin': self.fechaFin.strftime('%Y-%m-%d'),
            'equipo': self.equipo.serialize(),
            'ciclista': self.ciclista.serialize()
        }

# Modelo para la tabla Prueba
class Prueba(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    anioEdicion = db.Column(db.Integer, nullable=False)
    cantEtapas = db.Column(db.Integer, nullable=False)
    horaInicio = db.Column(db.DateTime, nullable=False)
    horaFin = db.Column(db.DateTime, nullable=False)
    kmTotal = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'anioEdicion': self.anioEdicion,
            'cantEtapas': self.cantEtapas,
            'horaInicio': self.horaInicio.strftime('%Y-%m-%d %H:%M:%S'),
            'horaFin': self.horaFin.strftime('%Y-%m-%d %H:%M:%S'),
            'kmTotal': self.kmTotal
        }

# Modelo para la tabla Inscripcion
class Inscripcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    puestoFinal = db.Column(db.Integer)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    prueba_id = db.Column(db.Integer, db.ForeignKey('prueba.id'), nullable=False)

    equipo = db.relationship('Equipo', backref='inscripciones')
    prueba = db.relationship('Prueba', backref='inscripciones')

    def serialize(self):
        return {
            'id': self.id,
            'fecha': self.fecha.strftime('%Y-%m-%d'),
            'numero': self.numero,
            'puestoFinal': self.puestoFinal,
            'equipo': self.equipo.serialize(),
            'prueba': self.prueba.serialize()
        }



