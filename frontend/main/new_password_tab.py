import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from backend.exceptions import IntegrityError
from backend.users import User
from backend import db_manager
from frontend.widgets import SuccessBox, ErrorBox
from frontend.forms import FormPrimaryButton
from frontend.main.widgets import TabHeader, TabLabel, TabTextInput


class NewPaswwordTab(qtw.QFrame):
    update_password_data = qtc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout()
        self.bind_widgets()
        self.render_ui()

    def set_layout(self):
        self.body = qtw.QGridLayout()
        self.body.setAlignment(qtc.Qt.AlignHCenter | qtc.Qt.AlignTop)
        self.body.setContentsMargins(277, 10, 277, 0)
        self.body.setVerticalSpacing(10)
        self.body.setHorizontalSpacing(10)
        self.setLayout(self.body)

    def bind_widgets(self):
        self.success_box = SuccessBox()

        self.app_name = TabTextInput(font_size=12)
        self.app_name.textChanged.connect(self.hide_error)

        self.url = TabTextInput(font_size=12)
        
        self.login = TabTextInput(font_size=12)

        self.email = TabTextInput(font_size=12)

        self.password = TabTextInput(font_size=12)

        self.master_password = TabTextInput(font_size=12)
        self.master_password.setEchoMode(qtw.QLineEdit.Password)
        self.master_password.textChanged.connect(self.hide_error)

        self.master_password_confirmed = TabTextInput(font_size=12)
        self.master_password_confirmed.setEchoMode(qtw.QLineEdit.Password)
        self.master_password_confirmed.textChanged.connect(self.hide_error)

        self.error_box = ErrorBox()

        self.submit_button = FormPrimaryButton('Submit', clicked=self.submit)

    def render_ui(self):
        self.body.addWidget(TabHeader('Add New Password', font_size=18), 0, 0, 1, 2)

        self.body.addWidget(self.success_box, 1, 0, 1, 2)

        self.body.addWidget(TabLabel('App Name*:', font_size=12), 2, 0)
        self.body.addWidget(self.app_name, 2, 1)
    
        self.body.addWidget(TabLabel('App Url:', font_size=12), 3, 0)
        self.body.addWidget(self.url, 3, 1)

        self.body.addWidget(TabLabel('Login:', font_size=12), 4, 0)       
        self.body.addWidget(self.login, 4, 1)

        self.body.addWidget(TabLabel('Email:', font_size=12), 5, 0)        
        self.body.addWidget(self.email, 5, 1)
    
        self.password.textChanged.connect(self.hide_error)
        self.body.addWidget(TabLabel('App Password*:', font_size=12), 6, 0)        
        self.body.addWidget(self.password, 6, 1)

        self.body.addWidget(TabLabel('Master Password*:', font_size=12), 7, 0)        
        self.body.addWidget(self.master_password, 7, 1)

        self.body.addWidget(TabLabel('Password Confirmed*:', font_size=12), 8, 0)        
        self.body.addWidget(self.master_password_confirmed, 8, 1)

        self.body.addWidget(self.error_box, 9, 0, 1, 2)
      
        self.body.addWidget(self.submit_button, 10, 0, 1, 2)

    def hide_error(self):
        if self.error_box.isHidden():
            return
        self.error_box.hide()

    def submit(self):
        self.hide_error()
        
        master_password = self.master_password.text()
        if not master_password or master_password != self.master_password_confirmed.text():
            return self.show_error('Master Passwords Not Match')

        password_data = {
            "app_name" : self.app_name.text().strip(),
            "url": self.url.text().strip(),
            "login": self.login.text().strip(),
            "email": self.email.text().strip(),
            "password": self.password.text().strip(),
        }

        try:
            db_manager.add_new_password(master_password, User.get_auth_data, password_data)
            self.clear_form()
            self.update_password_data.emit(True)
            self.show_success("You password was successfully added.")
        except IntegrityError as exc:
            self.show_error(str(exc))
    
    def clear_form(self):
        self.app_name.setText('')
        self.url.setText('')
        self.login.setText('')
        self.email.setText('')
        self.password.setText('')
        self.master_password.setText('')
        self.master_password_confirmed.setText('')

    def show_error(self, error):
        self.error_box.set_error(error)
        self.error_box.show()
    
    def show_success(self, msg):
        self.success_box.set_msg(msg)
        self.success_box.show()
        qtc.QTimer.singleShot(4000, self.success_box.hide)
    