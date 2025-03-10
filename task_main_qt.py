from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QMessageBox, QHBoxLayout, QDialog, QCalendarWidget
)
from PyQt6 import QtCore
import sys

from notion_funcs import build_notion_page

projects = [
    "UMC 2025",
    "401 2025",
    "Aesthetics",
    "Admin General",
    "Personal Random",
    "Reviewing",
    "Student Random",
    "Tactic",
    "Reddit Project",
    "Letters of rec",
    "CS+LS"
]

class DateArea(QWidget):
    def __init__(self, name, parent_layout, form_widget):
        super().__init__()
        self.form_widget = form_widget
        self.date_label = QLabel(f"{name}:")
        parent_layout.addWidget(self.date_label)

        layout = QHBoxLayout()
        self.date_entry = QLineEdit()
        self.date_entry.setPlaceholderText("YYYY-MM-DD")
        layout.addWidget(self.date_entry)

        self.calendar_button = QPushButton("📅")
        self.calendar_button.clicked.connect(self.show_calendar)
        layout.addWidget(self.calendar_button)

        parent_layout.addLayout(layout)

    def get_date(self):
        return self.date_entry.text()

    def set_date(self, date):
        self.date_entry.setText(date)

    def show_calendar(self):
        dialog = CalendarDialog(self, self.form_widget)
        if dialog.exec():  # This is now valid - QDialog has exec()
            selected_date = dialog.selected_date
            self.date_entry.setText(selected_date.toString(QtCore.Qt.DateFormat.ISODate))


class ProjectForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Form with Calendar")
        self.setGeometry(100, 100, 400, 250)
        self.center_window()

        layout = QVBoxLayout()

        # Name field
        self.name_label = QLabel("Name:")
        self.name_entry = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_entry)

        # Project dropdown
        self.project_label = QLabel("Project:")
        self.project_dropdown = QComboBox()
        self.project_dropdown.addItems(projects)
        layout.addWidget(self.project_label)
        layout.addWidget(self.project_dropdown)

        self.start_date_area = DateArea("Start Date", layout, self)
        self.due_date_area = DateArea("Due Date", layout, self)

        button_layout = QHBoxLayout()
        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)
        button_layout.addWidget(self.submit_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.geometry()

        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        self.move(x, y)

    def clear_form(self):
        self.name_entry.clear()
        self.start_date_area.set_date("")
        self.due_date_area.set_date("")
        self.project_dropdown.setCurrentIndex(0)

    def submit_form(self):
        name = self.name_entry.text()
        start_date = self.start_date_area.get_date()
        due_date = self.due_date_area.get_date()
        project = self.project_dropdown.currentText()

        if not name:
            QMessageBox.critical(self, "Error", "Name is required.")
            return

        print(f"Name: {name}")
        print(f"Start Date: {start_date}")
        print(f"Project: {project}")
        # QMessageBox.information(self, "Submitted", f"Name: {name}\nStart Date: {start_date}\nProject: {project}")
        build_notion_page(project, name, start_date, due_date)


class CalendarDialog(QDialog):
    def __init__(self, parent, form_widget):
        super().__init__(parent)

        self.setWindowTitle("Select Date")
        self.setGeometry(300, 300, 300, 250)

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar)

        self.setLayout(layout)

        # Initial date
        self.selected_date = self.calendar.selectedDate()

        # Connect the calendar click signal
        self.calendar.clicked.connect(self.date_selected)
        parent_pos = form_widget.mapToGlobal(parent.date_entry.pos())
        self.move(parent_pos.x(), parent_pos.y() + 30)

    def date_selected(self, date):
        self.selected_date = date
        self.accept()  # This will close the dialog and return control to the main window


app = QApplication(sys.argv)
form = ProjectForm()
form.show()
sys.exit(app.exec())

# to build
#  pyinstaller --noconsole --onedir --name "Notion Task" --windowed --add-data "notion_secret.txt:." task_main_qt.py

