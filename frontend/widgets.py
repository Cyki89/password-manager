import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc


class Label(qtw.QLabel):
    def __init__(self, *args, font_size=16, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_size = font_size
        self.set_config()
    
    def set_config(self):
        self.setFont(qtg.QFont('Arial', self.font_size))
        self.setAlignment(qtc.Qt.AlignCenter)


class ErrorBox(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, font_size=14, **kwargs)
    
    def set_config(self):
        super().set_config()
        self.hide()
    
    def set_error(self, error):
        self.setText(error)


class SuccessBox(Label):
    def __init__(self, *args, font_size=14, **kwargs):
        super().__init__(*args, font_size=font_size, **kwargs)
        self.set_config()
    
    def set_config(self):
        super().set_config()
        self.setContentsMargins(0, 0, 0, 10)
        self.hide()

    def set_msg(self, msg):
        self.setText(msg)


class Button(qtw.QPushButton):
    def __init__(self, *args, font_size=16, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_config(font_size)

    def set_config(self, font_size):
        self.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))
        self.setFont(qtg.QFont('Arial', font_size))


class CheckBox(qtw.QCheckBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_config()

    def set_config(self):
        self.setFont(qtg.QFont('Arial', 14))


class CheckBoxRight(CheckBox):
    def set_config(self):
        super().set_config()
        self.setLayoutDirection(qtc.Qt.RightToLeft)


class TextInput(qtw.QLineEdit):
    def __init__(self, *args, font_size=14, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_config(font_size)

    def set_config(self, font_size):
        ...

class TextOutput(qtw.QLineEdit):
    def __init__(self, *args, font_size=16, placeholder=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_config(font_size, placeholder)

    def set_config(self, font_size, placeholder):
        self.setFont(qtg.QFont('Arial', font_size))
        self.setPlaceholderText(placeholder)

class Frame(qtw.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout()
        self.set_config()
        self.bind_widgets()
        self.render_ui()

    def set_config(self):
        ...

    def set_layout(self):
        ...

    def bind_widgets(self):
        ...

    def render_ui(self):
        ...


class TabWidget(qtw.QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_config()
    
    def set_config(self):   
        self.setFont(qtg.QFont('Arial', 14))
        self.tabBar().setCursor(qtc.Qt.PointingHandCursor)

    def add_tabs(self, tabs):
        for tab in tabs:
            self.addTab(*tab)