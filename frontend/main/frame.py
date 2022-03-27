import PyQt5.QtWidgets as qtw

from frontend.main.password_data_tab import PasswordDataTab
from frontend.main.generate_password_tab import GeneratePaswwordTab
from frontend.main.new_password_tab import NewPaswwordTab
from backend.users import User
from frontend.utils import clear_layout
from frontend.widgets import Label, Frame, TabWidget


class MainFrame(Frame):   
    def set_config(self):
        self.setContentsMargins(0,0,0,0)

    def set_layout(self):
        self.body = qtw.QVBoxLayout()
        self.body.setContentsMargins(0,0,0,0)
        self.setLayout(self.body)
    
    def render_ui(self):
        clear_layout(self.body)
        
        if User.is_logged:
            return self.render_logged_in_user_ui()
       
        self.render_logged_out_user_ui()

    def render_logged_in_user_ui(self):
        self.tab_widget = TabWidget()
        self.body.addWidget(self.tab_widget)
        
        self.new_password_tab = NewPaswwordTab()      
        self.new_password_tab.update_password_data.connect(self.handle_update)
        
        self.tab_widget.add_tabs((
            (self.new_password_tab, 'New Password'),
            (GeneratePaswwordTab(), 'Generate Password'),
            (PasswordDataTab(), 'User Passwords'),
        ))

    def handle_update(self):
        self.tab_widget.removeTab(2)
        self.tab_widget.addTab(PasswordDataTab(), 'User Passwords')


    def render_logged_out_user_ui(self):
        self.body.addWidget(
            Label(text='You must be logged in to see any data', font_size=22)
        )
