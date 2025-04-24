import reflex as rx   

def notify_commponenet(mensaje: str, icon_notify: str, color: str) -> rx.Component:
    return rx.callout(
        mensaje,
        icon=icon_notify,
        style=style_notify,
        color_scheme=color
    )


style_notify = { 
    'background-color': '#f8d7da',
    'color': '#721c24',
    'border-color': '#f5c6cb',
    'padding': '10px',
    'border-radius': '5px',
    'margin': '10px 0'
}