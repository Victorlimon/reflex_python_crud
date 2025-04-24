import reflex as rx
from typing import TypedDict


# Definimos la estructura de una venta
class Venta(TypedDict):
    producto: str
    precio: float


class VentasState(rx.State):
    ventas: list[Venta] = [
        {"producto": "Laptop", "precio": 1200.0},
        {"producto": "Mouse", "precio": 25.0},
        {"producto": "Teclado", "precio": 45.0}
    ]


@rx.page(route="/ventas", title="Ventas")
def ventas_page() -> rx.Component:
    return rx.flex(
        rx.heading("Página de Ventas", align="center"),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Producto"),
                    rx.table.column_header_cell("Precio")
                )
            ),
            rx.table.body(
                rx.foreach(
                    VentasState.ventas,
                    lambda venta: rx.table.row(
                        rx.table.cell(venta["producto"]),
                        rx.table.cell(f"${venta['precio']:.2f}")
                    )
                )
            )
        ),
        direction="column",
        style={"width": "50vw", "margin": "auto", "margin-top": "50px"}
    )
