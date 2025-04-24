from ..model.usuario_model import usuario
from .connect_db import connect
from sqlmodel import Session, select

def select_all():
    engine = connect()
    with Session(engine) as session:
        query = select(usuario)
        result = session.exec(query).all()
        return result
    
def select_user_by_correo(correo: str):
    engine = connect()
    with Session(engine) as session:
        query = select(usuario).where(usuario.correo == correo)
        result = session.exec(query).all()
        return result

def create_user(user_obj: usuario):
    engine = connect()
    with Session(engine) as session:
        session.add(user_obj)
        session.commit()
        query = select(usuario)
        return session.exec(query).all()

def delete_user(correo: str):
    engine = connect()
    with Session(engine) as session:
        query = select(usuario).where(usuario.correo == correo)
        userdelete = session.exec(query).first()
        session.delete(userdelete)
        session.commit()
        query = select(usuario)
        return session.exec(query).all()

def update_user(user_obj: usuario):
    engine = connect()
    with Session(engine) as session:
        session.add(user_obj)
        session.commit()
        query = select(usuario).where(usuario.correo == user_obj.correo)
        result = session.exec(query).all()
        return result
