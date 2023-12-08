from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
)
import sys


class AverageSpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.distance_label = QLabel("Distance:")
        self.grid.addWidget(self.distance_label, 0, 0)

        self.distance_input = QLineEdit()
        self.grid.addWidget(self.distance_input, 0, 1)

        self.combo = QComboBox()
        self.combo.addItems(["km", "miles"])
        self.grid.addWidget(self.combo, 0, 2)

        self.time_label = QLabel("Time (hours):")
        self.grid.addWidget(self.time_label, 1, 0)

        self.time_input = QLineEdit()
        self.grid.addWidget(self.time_input, 1, 1)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_average_speed)
        self.grid.addWidget(self.calculate_button, 2, 0, 1, 3)

        # Define the label for average speed
        self.average_speed_label = QLabel("Average Speed: N/A")
        self.grid.addWidget(self.average_speed_label, 3, 0, 1, 3)

    def calculate_average_speed(self):
        try:
            distance = float(self.distance_input.text())
            time = float(self.time_input.text())

            if time == 0:
                self.average_speed_label.setText("Time can't be zero")
                return

            speed = distance / time
            unit = self.combo.currentText()

            self.average_speed_label.setText(f"Average Speed: {speed:.2f} {unit}/h")
        except ValueError:
            self.average_speed_label.setText(
                "Please enter valid numbers for distance and time."
            )


app = QApplication(sys.argv)
calculator = AverageSpeedCalculator()
calculator.show()
sys.exit(app.exec())
