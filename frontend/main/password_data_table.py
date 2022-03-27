import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from PyQt5.Qt import QUrl, QDesktopServices

from backend.users import User
from backend import db_manager
from frontend.styles import COLOR_PRIMARY, COLOR_GREEN, COLOR_RED
from frontend.main.password_data_forms import GetPasswordForm, EditPasswordForm, DeletePasswordForm


class ClickableTableWidget(qtw.QTableWidgetItem):
    def __init__(self, *args, parent=None, data=None, update_password_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.data = data
        self.update_password_data = update_password_data
        self.set_config()

    def set_config(self):
        ...

    def handle_click(self):
        self.do_handle_click()

    def do_handle_click(self):
        ...


class GetPasswordTableWidget(ClickableTableWidget):
    def set_config(self):
        super().set_config()
        self.setForeground(qtg.QColor(COLOR_PRIMARY))

    def do_handle_click(self):
        self.see_password_form = GetPasswordForm(self.parent, self.data, None)
        self.see_password_form.show()


class OpenUrlTableWidget(ClickableTableWidget):
    def set_config(self):
        super().set_config()

    def do_handle_click(self):
        QDesktopServices.openUrl(QUrl(self.data))


class EditPasswordTableWidget(ClickableTableWidget):
    def set_config(self):
        super().set_config()
        self.setForeground(qtg.QColor(COLOR_GREEN))

    def do_handle_click(self):
        self.edit_password_form = EditPasswordForm(self.parent, self.data, self.update_password_data)
        self.edit_password_form.show()


class DeletePasswordTableWidget(ClickableTableWidget):
    def set_config(self):
        super().set_config()
        self.setForeground(qtg.QColor(COLOR_RED))

    def do_handle_click(self):
        self.delete_form = DeletePasswordForm(self.parent, self.data, self.update_password_data)
        self.delete_form.show()


class TableWidget(qtw.QTableWidget):
    update_password_data = qtc.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    
        self.bind_events()

    def create_table(self, query_data):
        self.clear()
        
        passwords = list(db_manager.get_user_passwords(User._id, query_data))
        data_size = len(passwords)
        
        self.set_config(data_size)
        self.render_cells(passwords)
        self.align_cells(data_size)

    def set_config(self, data_size):
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(
            ['App Name', 'Url', 'Login', 'Email', 'Password', '', '']
        )
        self.setRowCount(max(data_size, 12))

        self.setFont(qtg.QFont('Arial', 12))
        self.horizontalHeader().setFont(qtg.QFont('Arial', 12))
        self.verticalHeader().setFont(qtg.QFont('Arial', 12))
        
        header = self.horizontalHeader()       
        for i in range(self.columnCount()):
            if i == 1:
                header.setSectionResizeMode(i, qtw.QHeaderView.Stretch)
            else:
                header.setSectionResizeMode(i, qtw.QHeaderView.ResizeToContents)
        
    def bind_events(self):
        self.setMouseTracking(True)
        self.cellEntered.connect(self.cell_hover)
        self.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
        self.itemClicked.connect(self.handle_click)

    def render_cells(self, data):
        for idx, row in enumerate(data):
            self.setItem(idx, 0, qtw.QTableWidgetItem(row['app_name']))
            self.setItem(idx, 1, OpenUrlTableWidget(row['url'], parent=self, data=row['url']))
            self.setItem(idx, 2, qtw.QTableWidgetItem(row['login']))
            self.setItem(idx, 3, qtw.QTableWidgetItem(row['email']))
            self.setItem(idx, 4, GetPasswordTableWidget('Show', parent=self,  data=row))
            self.setItem(idx, 5, EditPasswordTableWidget(
                'Edit', parent=self, update_password_data=self.update_password_data, data=row)
            )
            self.setItem(idx, 6, DeletePasswordTableWidget(
                'Delete', parent=self, update_password_data=self.update_password_data, data=row)
            )

    def align_cells(self, rows):
        cols = self.columnCount()
        for i in range(rows):
            for j in range(cols):
                self.item(i,j).setTextAlignment(qtc.Qt.AlignCenter)

    def handle_click(self, item):
        if not isinstance(item, ClickableTableWidget):
            return
        item.handle_click()

    def cell_hover(self, row, col):
        self.setCursor(qtg.QCursor(qtc.Qt.ArrowCursor))
        item = self.item(row, col)
        if isinstance(item, ClickableTableWidget):
            self.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))