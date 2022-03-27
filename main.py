import PyQt5.QtWidgets as qtw

import sys

from frontend.styles import STYLE_SHEET
from frontend.navbar.frame import NavbarFrame
from frontend.main.frame import MainFrame
from frontend.footer.frame import FooterFrame
from frontend.forms import LoginForm, RegisterForm


class MainWindow(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout()
        self.set_config()
        self.bind_widgets()
        self.bind_events()
        self.render_ui()
    
    def set_config(self):
        self.setWindowTitle('Password Manager App')
        self.setFixedSize(1024, 768)
        self.setStyleSheet(STYLE_SHEET) 
        
    def set_layout(self):
        self.body = qtw.QVBoxLayout()
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.setSpacing(0)
        self.setLayout(self.body)

    def bind_widgets(self):
        self.navbar = NavbarFrame()
        self.main = MainFrame()

        self.auth_container = self.navbar.auth_container

        self.login_form = LoginForm(self)
        self.register_form = RegisterForm(self)

    def bind_events(self):
        self.auth_container.open_login_form.connect(self.open_login_form)
        self.auth_container.open_register_form.connect(self.open_register_form)
        
        self.auth_container.user_logout.connect(self.auth_container.render_ui)
        self.auth_container.user_logout.connect(self.main.render_ui)
        
        self.login_form.user_login.connect(self.auth_container.render_ui)
        self.login_form.user_login.connect(self.main.render_ui)
        
        self.register_form.user_login.connect(self.auth_container.render_ui)
        self.register_form.user_login.connect(self.main.render_ui)

    def render_ui(self):
        self.body.addWidget(self.navbar, 1)
        self.body.addWidget(self.main, 10)
        self.body.addWidget(FooterFrame(), 1)

    def open_login_form(self):
        self.login_form.show()

    def open_register_form(self):
        self.register_form.show()


class App(qtw.QApplication):
    def __init__(self, window):
        super().__init__(sys.argv)
        self.window = window()
    
    def run(self):
        self.window.show()
        sys.exit(self.exec_())


if __name__ == '__main__':
    App(MainWindow).run()
