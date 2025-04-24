
import reflex as rx
from .api.api import hello


from rxconfig import config

class State(rx.State):
    # State
    @rx.var
    def say_hello(self) -> list[str]:
        return hello()
    ...



def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.foreach(State.say_hello, lambda msg: rx.text(msg, size="5")),
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )

app = rx.App()
app.add_page(index)

app.api.add_api_route("/hello", hello)
