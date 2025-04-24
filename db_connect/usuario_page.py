import reflex as rx 
from .model.usuario_model import usuario
from .service.usuario_service import select_all_usuario_service, select_user_by_correo_service, create_user_service, delete_user_service, update_user_service
from .notify import notify_commponenet
import asyncio
from typing import Callable, Optional


class UsuarioState(rx.State):
    #State
    usuarios:list[usuario] = []
    user_where: str = ''
    error: str = ''
    
    @rx.event(background=True)
    async def get_all_usuario(self):
        async with self:
            self.usuarios = select_all_usuario_service()

    @rx.event(background=True)
    async def get_correo_usuario(self):
        async with self:
            self.usuarios = select_user_by_correo_service(self.user_where)
    
    async def handleNotfy(self):
        async with self:
            await asyncio.sleep(2)
            self.error = ''
    
    @rx.event(background=True)
    async def create_usuario(self, data: dict):
        async with self:
            try:
                self.usuarios = create_user_service(correo=data['correo'], password=data['password'])
            except ValueError as e:
                self.error = str(e)
        await self.handleNotfy()

    @rx.event(background=True)
    async def delete_usuario(self, correo: str):
        async with self:
            self.usuarios = delete_user_service(correo)
    
    @rx.event(background=True)
    async def update_usuario(self, data: dict):
        async with self:
            try:
                user = select_user_by_correo_service(data['correo'])
                if len(user) != 0:
                    #user[0].password = data['password']
                    self.usuarios = update_user_service(data['correo'], data['password'])
                else:
                    self.error = 'El usuario no existe'
            except ValueError as e:
                self.error = str(e)
        await self.handleNotfy()



@rx.page(route='/usuario', title='usuario', on_load=UsuarioState.get_all_usuario)

def usuario_page() -> rx.Component:
    return rx.flex(
        rx.heading('Usuarios', align='center'),
        rx.hstack(
            search_usuario(),
            crear_usuario_dialogo(),
            justify='center',
            style={'margin-top': '30px'}
        ),
        table_usuario(UsuarioState.usuarios),
        rx.cond(
            UsuarioState.error != '',
            notify_commponenet(
                mensaje=UsuarioState.error,
                icon_notify='shield-alert',
                color='yellow'
            ),
        ),
        direction='column',
        style={'width': '60vw', 'margin': 'auto'}
        
    )


def table_usuario(list_usuario: list[usuario]) -> rx.Component:
    # Table
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell('Id_usuario'),
                rx.table.column_header_cell('Correo'),
                rx.table.column_header_cell('Password')
            )
        ),
        rx.table.body(
            rx.foreach(list_usuario, row_table)
        )
    )

def row_table(usuario: usuario) -> rx.Component:
    # Row Table
    return rx.table.row(
        rx.table.cell(usuario.id_usuario),
        rx.table.cell(usuario.correo),
        rx.table.cell(usuario.password),
        rx.table.cell(
            rx.hstack(
                delete_user_dialogo_component(usuario.correo),
                actualizar_usuario_dialogo(usuario.correo) 
            )
        )
    )


def search_usuario() -> rx.Component:
    return rx.hstack(
        rx.input(
            placeholder='Buscar por correo',
            value=UsuarioState.user_where,
            on_change=UsuarioState.set_user_where,
        ),
        rx.button('Buscar', on_click=UsuarioState.get_correo_usuario)
    )


def user_dialog_component(
    titulo: str,
    descripcion: str,
    boton_texto: str,
    submit_fn: Callable,
    trigger_text: str = "Abrir Diálogo",
    trigger_icon: str = "plus",
    text_value: Optional[str] = None,
    focus_but: Optional[bool] = None,

) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon(trigger_icon, size=14),
                rx.text(trigger_text, size="2"),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(titulo),
            rx.dialog.description(descripcion),
            rx.form(
                rx.flex(
                    rx.input(
                        type ="email",
                        placeholder="Correo",
                        name="correo",
                        # solo incluir `value` si `text_value` no es None
                        **({"value": text_value} if text_value is not None else {}),
                    ),
                    rx.input(
                        placeholder="Password",
                        name="password",
                        type="password",
                        **({"auto_focus": focus_but} if focus_but is not None else {}),
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button("Cancelar", variant="soft", color_scheme="gray"),
                        ),
                        rx.dialog.close(
                            rx.button(boton_texto, type="submit"),
                        ),
                        spacing="3",
                        justify="end",
                    ),
                    direction="column",
                    spacing="4",
                ),
                on_submit=submit_fn,
                reset_on_submit=False,
            ),
            max_width="450px",
        ),
    )


def crear_usuario_dialogo() -> rx.Component:
    return user_dialog_component(
        titulo="Añadir nuevo usuario",
        descripcion="Rellene el formulario con los datos del usuario",
        boton_texto="Crear",
        submit_fn=UsuarioState.create_usuario,
        trigger_text="Crear Usuario",
        trigger_icon="plus",
    )


def actualizar_usuario_dialogo(correo: str) -> rx.Component:
    return user_dialog_component(
        titulo="Cambiar Contraseña",
        descripcion="Modifique los datos necesarios",
        boton_texto="Actualizar",
        submit_fn=UsuarioState.update_usuario,
        trigger_text="Cambiar Contraseña",
        trigger_icon="pencil",
        text_value=correo,
        focus_but= True,
    )


def delete_user_dialogo_component(correo) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("trash", size=14),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Eliminar usuario",
            ),
            rx.dialog.description(
                "¿Está seguro de que desea eliminar este usuario?",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Confirmar", 
                        type="submit",
                        on_click=UsuarioState.delete_usuario(correo),
                    ),
                ),
                spacing="3",
                justify="end",
            ),
            max_width="450px",
        ),
    )

