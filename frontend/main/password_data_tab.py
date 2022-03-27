import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from frontend.widgets import SuccessBox
from frontend.main.password_data_search_widget import SearchWidget 
from frontend.main.password_data_table import TableWidget


class PasswordDataTab(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query_data = {}
        self.set_layout()
        self.bind_widgets()
        self.bind_events()
        self.render_ui()

    def set_layout(self):
        self.body = qtw.QVBoxLayout()
        self.body.setContentsMargins(0, 10, 0, 0)
        self.body.setAlignment(qtc.Qt.AlignHCenter | qtc.Qt.AlignTop)
        self.body.setSpacing(0)
        self.setLayout(self.body)

    def bind_widgets(self):
        self.success_box = SuccessBox()
        self.search_box = SearchWidget()
        self.table = TableWidget()
    
    def bind_events(self):
        self.search_box.search_request.connect(self.handle_search_request)
        self.table.update_password_data.connect(self.handle_update_data)

    def render_ui(self):
        self.body.addWidget(self.success_box)     
        self.body.addWidget(self.search_box)
        self.body.addWidget(self.table)
        
        self.table.create_table(self.query_data)

    def handle_search_request(self, query_data):
        self.query_data = query_data
        self.table.create_table(self.query_data)

    def handle_update_data(self, msg):
        self.table.create_table(self.query_data)
        self.show_success(msg)

    def show_success(self, msg):
        self.success_box.set_msg(msg)
        self.success_box.show()
        qtc.QTimer.singleShot(4000, self.success_box.hide)
