from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QGridLayout,
    QLineEdit,
    QPushButton,
)
import sys
from datetime import datetime


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()

        self.setWindowTitle("Age Calculator")

        # create widget
        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        date_of_birth_label = QLabel("Date of Birth MM/DD/YYYY: ")
        self.date_of_birth_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate)
        self.output_label = QLabel("")

        # add widget to grid

        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(date_of_birth_label, 1, 0)
        grid.addWidget(self.date_of_birth_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate(self):
        current_year = datetime.now().year
        year_of_birth = int(self.date_of_birth_line_edit.text().split("/")[2])
        age = current_year - year_of_birth
        self.output_label.setText(f"{self.name_line_edit.text()} is {age} years old.")


app = QApplication(sys.argv)

calculator = AgeCalculator()

calculator.show()

sys.exit(app.exec())
