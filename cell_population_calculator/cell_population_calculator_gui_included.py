# sys module provides access to system-specific parameters and functions that interact with the Python interpreter
import sys
# import pyqt6 library
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit)

class CellSimulator(QWidget):
  #
  def __init__(self):
    super().__init__()
    self.init_ui()
  #
  def init_ui(self):
    self.setWindowTitle("Zellwachstum Simulator")
    self.resize(300, 350)

    layout = QVBoxLayout()

    # Input: Startpopulation
    self.label_cells = QLabel("Cell population at the beginning")
    self.input_cells = QLineEdit()
