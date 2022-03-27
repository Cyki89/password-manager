import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from backend.users import User

from frontend.utils import clear_layout
from frontend.navbar.widgets import NavbarLabel, NavbarBrandLabel, NavbarButton, NavbarContainer
from frontend.widgets import Frame

  
class LogoNavbarContainer(NavbarContainer):
    def render_ui(self):
        self.body.addWidget(NavbarBrandLabel(text='Password Manager'))


class AuthNavbarContainer(NavbarContainer):
    open_login_form = qtc.pyqtSignal(bool)
    open_register_form = qtc.pyqtSignal(bool)
    user_logout = qtc.pyqtSignal(bool)

    def render_ui(self):
        clear_layout(self.body)

        if User.is_logged:
            return self.render_logged_in_user_ui()

        self.render_logged_out_user_ui()
        
    def render_logged_in_user_ui(self):
        self.body.addWidget(NavbarLabel(text=User.username))
        self.body.addWidget(NavbarButton('Logout', clicked=self.handle_logout_user))

    def render_logged_out_user_ui(self):
        self.body.addWidget(NavbarButton('Login', clicked=self.open_login_form))
        self.body.addWidget(NavbarButton('Register', clicked=self.open_register_form))

    def handle_logout_user(self):
        User.logout_user()
        self.user_logout.emit(True)


class NavbarFrame(Frame):
    def set_layout(self):
        self.body = qtw.QHBoxLayout()
        self.body.setSpacing(400)
        self.setLayout(self.body)

    def bind_widgets(self):
        self.auth_container = AuthNavbarContainer()
    
    def render_ui(self):
        self.body.addWidget(LogoNavbarContainer())
        self.body.addWidget(self.auth_container)