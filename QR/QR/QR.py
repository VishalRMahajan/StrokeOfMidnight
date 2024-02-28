from rxconfig import config
import pyqrcode
import reflex as rx

OuputPath= "F:\OpenProject\QR\QR\output"

class State(rx.State):
    """The app state."""
    link : str 
    form_data: dict = {}
    

    def handle_submit(self, form_data: dict) -> bool:
        self.link = form_data.get("link")
        if form_data.get("scale") == "":
            self.scale = 10
        else:
            self.scale = form_data.get("scale")
        qr = pyqrcode.create(self.link)
        qr.png( OuputPath + "\myqr.png", scale= int(self.scale))
        
    

def index() -> rx.Component:
      return rx.center(
        rx.flex(
            rx.form.root(
                rx.form.field(
                    rx.form.label("Link of which you want to generate QR Code"),
                    rx.form.control(
                        rx.input.input(
                            placeholder="Enter the link",
                            name="link", 
                            required=True,
                        ),
                        as_child=True,
                    ),
                    name="link",
                ),
                rx.form.field(
                    rx.form.label("Scale of the QR Code"),
                    rx.form.control(
                        rx.input.input(
                            placeholder="Enter the Scale",
                            name="scale", 
                        ),
                        as_child=True,
                    ),
                    name="scale",
                ),
                rx.form.submit(
                    rx.button(
                        "Create QR Code",
                    ),
                    as_child=True,
                ),
                rx.image(),
                on_submit=State.handle_submit,
                spacing="4",
            ),
            padding="2em",
            class_name="bg-white backdrop-blur-md rounded-lg shadow-lg",
            direction="column",
            spacing="2",
            align="center",
        ),
        width="100%",
        height="100vh",
        bg_color="#0a192f",
    )


app = rx.App()


app.add_page(index)
