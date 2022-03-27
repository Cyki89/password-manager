import PyQt5.QtWidgets as qtw

from frontend.widgets import Label, Button

class NavbarLabel(Label):
    ...


class NavbarBrandLabel(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, font_size=18, **kwargs)


class NavbarButton(Button):
    ...


class NavbarContainer(qtw.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout()
        self.render_ui()
    
    def set_layout(self):     
        self.body = qtw.QHBoxLayout()
        self.setLayout(self.body)
        self.body.setContentsMargins(20, 0, 20, 0)
