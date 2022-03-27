import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from frontend.forms import FormPrimaryButton
from frontend.main.widgets import TabTextInput


class SearchWidget(qtw.QWidget):
    search_request = qtc.pyqtSignal(dict)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout()
        self.bind_widgets()
        self.bind_events()
        self.render_ui()

    def bind_widgets(self):
        self.app_name = TabTextInput(parent=self, font_size=12)
        self.app_name.setPlaceholderText("App Name")

        self.login = TabTextInput(font_size=12)
        self.login.setPlaceholderText("Login")

        self.email = TabTextInput(font_size=12)
        self.email.setPlaceholderText("Email")

        self.search_button = FormPrimaryButton(text="Search", font_size=16)
    
    def bind_events(self):
        self.search_button.clicked.connect(self.search)

    def set_layout(self):
        self.body = qtw.QHBoxLayout()
        self.body.setSpacing(30)
        self.body.setContentsMargins(20, 0, 20, 10)
        self.body.setAlignment(qtc.Qt.AlignHCenter | qtc.Qt.AlignTop)
        self.setLayout(self.body)
    
    def render_ui(self):
        self.body.addWidget(self.app_name)
        self.body.addWidget(self.login)
        self.body.addWidget(self.email)
        self.body.addWidget(self.search_button)

    def search(self):
        query_data = {}
        app_name, login, email = (
            self.app_name.text(), self.login.text(), self.email.text()
        ) 

        if app_name:
            query_data['app_name'] = {'$regex': f'.*{app_name}.*', "$options": "i"}

        if login:
            query_data['login'] = {'$regex': f'.*{login}.*', "$options": "i"}

        if email:
            query_data['email'] = {'$regex': f'.*{email}.*', "$options": "i"}

        self.search_request.emit(query_data)
