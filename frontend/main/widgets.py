from frontend.widgets import Label, TextInput, TextOutput
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc


class TabLabel(Label):
    def set_config(self):
        self.setFont(qtg.QFont('Arial', self.font_size))


class TabTextInput(TextInput):
    def set_config(self, font_size):
        self.setFont(qtg.QFont('Arial', font_size))
        self.setMaximumWidth(250)


class TabTextOutput(TextOutput):
    ...


class TabHeader(Label):
    def __init__(self, *args, font_size=22, **kwargs):
        super().__init__(*args, font_size=font_size, **kwargs)


class Slider(qtw.QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(qtc.Qt.Horizontal, *args, **kwargs)
        self.set_config()

    def set_config(self):
        self.setMinimum(8)
        self.setMaximum(20)
        self.setMaximumWidth(350)