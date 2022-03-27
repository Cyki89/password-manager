import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

from backend.users import User
from backend.exceptions import IntegrityError, ObjectDoesNotFound

from frontend.widgets import Label, Button, ErrorBox, TextInput, TextOutput


class FormLabel(Label):
    ...


class FormHeader(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, font_size=22, **kwargs)


class FormTextInput(TextInput):
    def set_config(self, font_size):
        self.setMinimumWidth(320)
        self.setFont(qtg.QFont('Arial', font_size))


class FormTextOutput(TextOutput):
    ...


class FormPrimaryButton(Button):
    ...


class FormApproveButton(Button):
    ...


class FormCancelButton(Button):
    ...


class ModalForm(qtw.QDialog):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, qtc.Qt.WindowCloseButtonHint, *args, **kwargs)
        self.set_config()
        self.set_layout()
        self.render_ui()
        self.bind_events()

    def set_config(self):
        self.setContentsMargins(15, 10, 15, 15)
        self.setModal(True)

    def set_layout(self):
        self.body = qtw.QFormLayout()
        self.body.setVerticalSpacing(20)
        self.setLayout(self.body)

    def render_ui(self):
        ...

    def bind_events(self):
        ...


class AuthModalForm(ModalForm):
    user_login = qtc.pyqtSignal(bool)

    def render_ui(self):
        self.username = FormTextInput()
        self.username.textChanged.connect(self.hide_error)
        self.body.addRow(FormLabel("Username:"), self.username)

        self.email = FormTextInput()
        self.email.textChanged.connect(self.hide_error)
        self.body.addRow(FormLabel("Email:"), self.email)

        self.error_box = ErrorBox()
        self.body.addRow(self.error_box)

        self.body.addRow(FormPrimaryButton("Submit", clicked=self.submit))
  
    def hide_error(self):
        if self.error_box.isHidden():
            return
        self.error_box.hide()

    def bind_events(self):
        self.finished.connect(self.clear_form)

    def clear_form(self):
        self.username.setText('')
        self.email.setText('')
        self.hide_error()


class LoginForm(AuthModalForm):
    def render_ui(self):
        self.body.addRow(FormHeader("Login Form"))
        super().render_ui()

    def submit(self):
        try:
            User.login_user({'username': self.username.text(), 'email': self.email.text()})
            self.user_login.emit(True)
            self.close()
        except ObjectDoesNotFound as exc:
            self.error_box.set_error(str(exc))
            self.error_box.show()


class RegisterForm(AuthModalForm):
    def render_ui(self):
        self.body.addRow(FormHeader("Register Form"))
        super().render_ui()

    def submit(self):
        try:
            User.register_user({'username': self.username.text(), 'email': self.email.text()})
            self.user_login.emit(True)
            self.close()
        except IntegrityError as exc:
            self.error_box.set_error(str(exc))
            self.error_box.show()