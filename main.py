import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QVBoxLayout,
    QToolBar,
    QStatusBar,
)

from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setGeometry(500, 500, 500, 500)

        # Create menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Create actions for menu items
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert_data)
        file_menu_item.addAction(add_student_action)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search_action)
        edit_menu_item.addAction(search_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # Create the table widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create the toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create the status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def search_action(self):
        """Open the search dialog"""
        dialog = SearchDialog()
        dialog.exec()

    def load_data(self):
        """Load data from the database and populate the table"""
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        query = "SELECT * FROM students"
        result = cursor.execute(query)

        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )
        connection.close()

    def insert_data(self):
        """Open the insert dialog"""
        dialog = InsertDialog()
        dialog.exec()

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit_record)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete_record)

        children = self.findChildren(QPushButton)
        for child in children:
            self.status_bar.removeWidget(child)

        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    def edit_record(self):
        dialog = EditDialog()
        dialog.exec()

    def delete_record(self):
        dialog = DeleteDialog()
        dialog.exec()


class EditDialog(QDialog):
    """
    Dialog for editing student data.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("IUpdate Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        index = main_window.table.currentRow()
        self.student_id = main_window.table.item(index, 0).text()
        self.holder_name = main_window.table.item(index, 1).text()
        self.holder_mobile = main_window.table.item(index, 3).text()
        # Input field for student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText(f"{self.holder_name}")
        layout.addWidget(self.student_name)

        # Dropdown for student course
        self.student_course = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.student_course.addItems(courses)
        layout.addWidget(self.student_course)

        # Input field for student mobile
        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText(f"{self.holder_mobile}")
        layout.addWidget(self.student_mobile)

        # Submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.edit_student)
        layout.addWidget(button)

    def edit_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        query = "UPDATE students SET name=?, course=?, mobile=? WHERE id=?"
        cursor.execute(
            query,
            (
                self.student_name.text(),
                self.student_course.currentText(),
                self.student_mobile.text(),
                self.student_id,
            ),
        )
        connection.commit()
        connection.close()
        main_window.load_data()
        
class DeleteDialog(QDialog):
    pass


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Name")
        layout.addWidget(self.search_input)

        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

    def search_student(self):
        """Search for a student in the database"""
        name = self.search_input.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        query = "SELECT * FROM students WHERE name=?"
        result = cursor.execute(query, (name,))
        rows = result.fetchall()

        # Select the matching rows in the main table
        items = main_window.table.findItems(name, QtCore.Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()
        return rows


class InsertDialog(QDialog):
    """
    Dialog for inserting student data.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Input field for student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Enter Name")
        layout.addWidget(self.student_name)

        # Dropdown for student course
        self.student_course = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.student_course.addItems(courses)
        layout.addWidget(self.student_course)

        # Input field for student mobile
        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText("Enter Mobile")
        layout.addWidget(self.student_mobile)

        # Submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

    def add_student(self):
        """
        Add student data to the database.
        """
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        query = "INSERT INTO 'students'(name, course, mobile) VALUES(?, ?, ?)"
        cursor.execute(
            query,
            (
                self.student_name.text(),
                self.student_course.currentText(),
                self.student_mobile.text(),
            ),
        )
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
