import PyQt5.QtWidgets as qtw
from PyQt5.Qt import QUrl, QDesktopServices

from frontend.widgets import Frame
from frontend.navbar.widgets import NavbarButton

class FooterFrame(Frame):   
    def set_layout(self):
        self.body = qtw.QHBoxLayout()
        self.setLayout(self.body)
    
    def render_ui(self):
        self.link_button = NavbarButton(
            '>> Go to my other repos >>',
            font_size=14,
            clicked = lambda: QDesktopServices.openUrl(QUrl('https://github.com/Cyki89'))
        )       
        self.body.addWidget(self.link_button)