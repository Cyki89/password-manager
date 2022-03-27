import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from backend.exceptions import IntegrityError
from backend.users import User
from backend import password_manager
from backend import db_manager
from frontend.widgets import SuccessBox, ErrorBox
from frontend.forms import FormLabel, FormHeader, FormTextInput, FormTextOutput, FormPrimaryButton, FormApproveButton, FormCancelButton
from frontend.main.widgets import TabTextInput


class PasswordDataForm(qtw.QDialog):
    def __init__(self, parent, data, update_password_data, *args, **kwargs):
        super().__init__(parent, qtc.Qt.WindowCloseButtonHint, *args, **kwargs)
        self.data = data
        self.update_password_data=update_password_data
        self.set_layout()
        self.set_config()
        self.bind_widgets()
        self.bind_events()
        self.render_ui()

    def set_config(self):
        self.setWindowTitle('Password Data Form')
        self.setContentsMargins(15, 10, 15, 15)
        self.setModal(True)

    def set_layout(self):
        self.body = qtw.QFormLayout()
        self.body.setVerticalSpacing(20)
        self.setLayout(self.body)

    def render_ui(self):
        ...


class GetPasswordForm(PasswordDataForm):
    def bind_widgets(self):
        self.success_box = SuccessBox()
        
        self.decrypted_password = FormTextOutput(font_size=14)
        self.decrypted_password.setPlaceholderText('Your Password')
        self.copy_button = FormPrimaryButton('Copy')

        self.master_password = TabTextInput()
        self.master_password.setObjectName('DarkTabTextInput')
        self.master_password.setEchoMode(qtw.QLineEdit.Password)

        self.error_box = ErrorBox()

        self.submit_button = FormPrimaryButton("Show")

    def bind_events(self):
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        self.master_password.textChanged.connect(self.hide_error)

        self.submit_button.clicked.connect(self.submit)

    def render_ui(self):
        self.body.addRow(FormHeader(f"See password for {self.data['app_name']}"))

        self.body.addRow(self.success_box)

        self.body.addRow(self.decrypted_password, self.copy_button)

        self.body.addRow(FormLabel("Master password:", font_size=14), self.master_password)

        self.body.addRow(self.error_box)

        self.body.addRow(self.submit_button)

    def hide_error(self):
        if self.error_box.isHidden():
            return
        self.error_box.hide()

    def submit(self):
        try:
            password_decrypted = db_manager.get_password(
                User.salt, self.data['password'], self.master_password.text()
            )
            self.decrypted_password.setText(password_decrypted)
        except IntegrityError as exc:
            self.show_error(str(exc))

    def show_error(self, error):
        self.error_box.set_error(error)
        self.error_box.show()
    
    def show_success(self, msg):
        self.success_box.set_msg(msg)
        self.success_box.show()
        qtc.QTimer.singleShot(4000, self.success_box.hide)
    
    def copy_to_clipboard(self):
        txt = self.decrypted_password.text()
        if not txt:
            return    
        password_manager.copy_to_clipboard(txt)
        self.show_success("Password was copied to clipboard")


class EditPasswordForm(PasswordDataForm):
    def bind_widgets(self):
        self.success_box = SuccessBox()

        self.app_name = FormTextInput(self.data['app_name'])

        self.url = FormTextInput(self.data['url'])

        self.login = FormTextInput(self.data['login'])

        self.email = FormTextInput(self.data['email'])

        self.password = FormTextInput()

        self.master_password = FormTextInput()
        self.master_password.setEchoMode(qtw.QLineEdit.Password)

        self.error_box = ErrorBox()

        self.submit_button = FormPrimaryButton("Edit")

    def bind_events(self):
        self.app_name.textChanged.connect(self.hide_error)
        self.url.textChanged.connect(self.hide_error)
        self.login.textChanged.connect(self.hide_error)
        self.email.textChanged.connect(self.hide_error)
        self.password.textChanged.connect(self.hide_error)

        self.master_password.textChanged.connect(self.hide_error)

        self.submit_button.clicked.connect(self.submit)

    def render_ui(self):
        self.body.addRow(FormHeader(f"Edit Data for {self.data['app_name']}"))

        self.body.addRow(self.success_box)
        
        self.body.addRow(FormLabel("App Name:", font_size=14), self.app_name)
        self.body.addRow(FormLabel("Url:", font_size=14), self.url)
        self.body.addRow(FormLabel("Login:", font_size=14), self.login)
        self.body.addRow(FormLabel("Email:", font_size=14), self.email)
        self.body.addRow(FormLabel("Password:", font_size=14), self.password)

        self.body.addRow(FormLabel("Master password:", font_size=14), self.master_password)

        self.body.addRow(self.error_box)

        self.body.addRow(self.submit_button)

    def hide_error(self):
        if self.error_box.isHidden():
            return
        self.error_box.hide()

    def submit(self):
        password_data = self.get_data_from_inputs()
        try:
            db_manager.update_password_data(
                self.data['_id'], User.salt, self.master_password.text(), self.data['password'], password_data
            )
            self.update_password_data.emit("Your password was successfully updated")
            self.close()
        except IntegrityError as exc:
            self.show_error(str(exc))

    def get_data_from_inputs(self):
        inputs = [('app_name', self.app_name), ('url', self.url), ('login', self.login), 
                  ('email', self.email), ('password', self.password)]
        password_data = {
            label: txt for label, input in inputs if (txt := input.text()) and txt != self.data[label]
        }
        return password_data

    def show_error(self, error):
        self.error_box.set_error(error)
        self.error_box.show()


class DeletePasswordForm(PasswordDataForm):
    def set_config(self):
        super().set_config()
        self.body.setFieldGrowthPolicy(qtw.QFormLayout.FieldsStayAtSizeHint)

    def bind_widgets(self):
        self.submit_button = FormApproveButton("Yes")
        self.cancel_button = FormCancelButton("No")

    def bind_events(self):
        self.submit_button.clicked.connect(self.submit)
        self.cancel_button.clicked.connect(lambda: self.close())

    def render_ui(self):
        self.body.addRow(FormLabel(f"Are you sure to delete data for {self.data['app_name']}?"))

        self.body.addRow(self.submit_button, self.cancel_button)

    def submit(self):
        db_manager.delete_password_data(self.data["_id"])
        self.update_password_data.emit("Your password was successfully removed")
        self.close()
