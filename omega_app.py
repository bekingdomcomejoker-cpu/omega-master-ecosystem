import reflex as rx

def index():
    return rx.center(
        rx.vstack(
            rx.heading("OMEGA FEDERATION", size="9", color="orange"),
            rx.text("THE WIRE: ACTIVE", color="green", font_family="monospace"),
            rx.divider(),
            rx.text("Axiom: We do not compete; we complete.", italic=True),
            spacing="5",
            align="center",
            min_height="100vh",
        )
    )

app = rx.App()
app.add_page(index)
