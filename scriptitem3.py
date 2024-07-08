from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
import json

# Configuración de la base de datos
DATABASE_URL = "sqlite:///usuarios.db"

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Configuración del servidor web
app = Flask(__name__)

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    nombre = request.json['nombre']
    password = request.json['password']
    
    # Hash de la contraseña
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    nuevo_usuario = Usuario(nombre=nombre, password_hash=password_hash.decode('utf-8'))
    session.add(nuevo_usuario)
    session.commit()
    
    return app.response_class(
        response=json.dumps({'mensaje': 'Usuario creado con éxito'}, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    nombre = request.json['nombre']
    password = request.json['password']
    
    usuario = session.query(Usuario).filter_by(nombre=nombre).first()
    
    if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
        return app.response_class(
            response=json.dumps({'mensaje': 'Validación exitosa'}, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )
    else:
        return app.response_class(
            response=json.dumps({'mensaje': 'Nombre de usuario o contraseña incorrectos'}, ensure_ascii=False),
            status=401,
            mimetype='application/json'
        )

if __name__ == '__main__':
    app.run(host='192.168.1.213', port=5800)
