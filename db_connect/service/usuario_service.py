from ..repository.usuario_repository import select_all, select_user_by_correo, create_user, delete_user, update_user
from ..model.usuario_model import usuario

def select_all_usuario_service():
    usuario = select_all()
    return usuario

def select_user_by_correo_service(correo: str):
    if(len(correo) != 0):
        return select_user_by_correo(correo)
    else:
        return select_all()

def create_user_service(correo: str, password: str):
    user = select_user_by_correo(correo)
    if (len(user) == 0 ):
        user_save = usuario(correo=correo, password=password)
        return create_user(user_save)
    else:
        raise ValueError("El correo ya existe")


def delete_user_service(correo: str):
    return delete_user(correo=correo)

def update_user_service(correo: str, password: str):
    usuarios = select_user_by_correo(correo)
    
    if usuarios:
        usuario = usuarios[0]
        usuario.password = password
        return update_user(usuario)
    else:
        raise ValueError(f"El correo '{correo}' no existe.")


