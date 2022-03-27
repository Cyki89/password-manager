import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

from backend import password_manager
from frontend.widgets import CheckBox, CheckBoxRight, ErrorBox, SuccessBox
from frontend.forms import FormPrimaryButton
from frontend.main.widgets import TabHeader, TabLabel, TabTextOutput, Slider


class GeneratePaswwordTab(qtw.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout()
        self.bind_widgets()
        self.render_ui()

    def set_layout(self):
        self.body = qtw.QGridLayout()
        self.body.setAlignment(qtc.Qt.AlignHCenter | qtc.Qt.AlignTop)
        self.body.setContentsMargins(0, 10, 0, 0)
        self.body.setVerticalSpacing(15)
        self.body.setHorizontalSpacing(10)
        self.setLayout(self.body)

    def bind_widgets(self):
        self.success_box = SuccessBox()

        self.generated_password = TabTextOutput(placeholder='Your Password', font_size=14)
        self.copy_button = FormPrimaryButton('Copy', clicked=self.copy_to_clipboard)
        
        self.length = Slider()
        self.length.valueChanged.connect(self.change_password_length)
        self.length_label = TabLabel(f'Length: {self.length.value():2}', font_size=14)

        self.lower_letters = CheckBox('Contains Lower Letters')
        self.digits = CheckBoxRight('Contains Digits')

        self.upper_letters = CheckBox('Contains Upper Letters')
        self.symbols = CheckBoxRight('Contains Symbols')

        self.error_box = ErrorBox()

        self.submit_button = FormPrimaryButton("Generate Password", font_size=18, clicked=self.generate_password)

    def render_ui(self):
        self.body.addWidget(TabHeader('Generate Strong Password'), 0, 0, 1, 4)

        self.body.addWidget(self.success_box, 1, 0, 1, 4 )

        self.body.addWidget(self.generated_password, 2, 0, 1,3 )
        self.body.addWidget(self.copy_button, 2, 3)
  
        self.body.addWidget(self.length_label, 3, 0)
        self.body.addWidget(self.length, 3, 1, 1, 3)

        self.body.addWidget(self.lower_letters, 4, 0, 1, 2)
        self.body.addWidget(self.digits, 4, 2, 1, 2)

        self.body.addWidget(self.upper_letters, 5, 0, 1, 2)
        self.body.addWidget(self.symbols, 5, 2, 1, 2)

        self.body.addWidget(self.error_box, 6, 0, 1, 4)
       
        self.body.addWidget(self.submit_button, 7, 0, 1, 4)

    def hide_error(self):
        if self.error_box.isHidden():
            return
        self.error_box.hide()
    
    def show_success(self, msg):
        self.success_box.set_msg(msg)
        self.success_box.show()
        qtc.QTimer.singleShot(4000, self.success_box.hide)

    def change_password_length(self):
        self.length_label.setText(f'Length: {self.length.value()}')

    def copy_to_clipboard(self):
        txt = self.generated_password.text()
        if not txt:
            return
        password_manager.copy_to_clipboard(txt)
        self.show_success('Your password was coppied to the clipboard')

    def generate_password(self):
        self.hide_error()

        options = {
            'length': self.length.value(),
            'contain_lower' : self.lower_letters.isChecked(),
            'contain_upper' : self.upper_letters.isChecked(),
            'contain_digits' : self.digits.isChecked(),
            'contain_symbols' : self.symbols.isChecked(),
        }
        try:
            password = password_manager.generate_password(**options)
            self.generated_password.setText(password)
        except ValueError as exc:
            self.error_box.set_error(str(exc))
            self.error_box.show()

