# sys module provides access to system-specific parameters and functions that interact with the Python interpreter
import sys
# import pyqt6 library
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit)

class CellSimulator(QWidget):
  # initialisation function
  def __init__(self):
    super().__init__()
    self.init_ui()
  # 
  def init_ui(self):
    self.setWindowTitle("Cellgrowth Simulator")
    self.resize(300, 300)

    layout = QVBoxLayout()

    # Input: Startpopulation
    self.label_cells = QLabel("Cell population at the beginning:")
    self.input_cells = QLineEdit()
    layout.addWidget(self.label_cells)
    layout.addWidget(self.input_cells)

    # Input: Days
    self.label_days = QLabel("Days since observation:")
    self.input_days = QLineEdit()
    layout.addWidget(self.label_days)
    layout.addWidget(self.input_days)

    # Start Button 
    self.btn_calc = QPushButton("Berechnen")
    self.btn_calc.clicked.connect(self.calculate_growth)
    layout.addWidget(self.btn_calc)

    # Output field
    self.output_area = QTextEdit()
    self.output_area.setReadOnly(True)
    layout.addWidget(self.output_area)

    self.setLayout(layout)

  # Function for calculation
  def calculate_growth(self):
    self.output_area.clear()
    # input cells and days
    try:
     cells = int(self.input_cells.text())
     days = int(self.input_days.text())
    except ValueError:
     self.ouput_area.setText("Insert numbers, please.")
     return
    # counter
    counter = 1
    while counter <= days:
     cells = cells * 2
     self.output_area.append(f"Day {counter}: {cells}")
     counter = counter + 1

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = CellSimulator()
  window.show()
  sys.exit(app.exec())
