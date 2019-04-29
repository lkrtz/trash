import sys
from functools import partial

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSlot


WINDOW_NAME = "Telephone mask example"
W_SIZE = 1200
H_SIZE = 600

MIN_WIDTH = 1280
MIN_HEIGHT = 768

class MainWindow(QMainWindow):
    """
    Qt widget for Main window
    Initializing window and showing test image
    """

    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(MIN_WIDTH, MIN_HEIGHT)

        self.label = QLabel(self)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(500, 20)
        self.textbox.resize(280, 40)

        mask = "+7 (000) 000 00 00"
        self.textbox.setText(mask)
        self.textbox.setMaxLength(len(mask))
        self.maxSize = len(self.textbox.text())
        self.textImmutable = []
        for i in range(len(self.textbox.text())):
            if self.textbox.text()[i] == "0":
                continue
            self.textImmutable.append(i)

        # Create cursor and set to first position in textbox
        self.textbox.setCursorPosition(0)

        # Create digit and delete buttons
        buttonCoordX = 500
        buttonCoordY = 80
        buttonSize = 30
        counter = 0
        self.button = list()
        for i in range(10):
            self.button.append(QPushButton(str(9 - i), self))
            self.button[i].resize(buttonSize, buttonSize)
            self.button[i].move(buttonCoordX - buttonSize*counter,
                                buttonCoordY + buttonSize
                                )
            counter += 1
            self.button[i].clicked.connect(
               partial(self.add_click, 9-i)
            )
            if counter == 3:
                counter = 0
                buttonCoordY += buttonSize

        # Delete button
        self.delButton = QPushButton("<x", self)
        self.delButton.clicked.connect(self.del_click)

        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(500, 500, W_SIZE, H_SIZE)
        self.setWindowTitle(WINDOW_NAME)

        self.show()

    @pyqtSlot()
    def add_click(self, digit: int) -> None:
        position = self.textbox.cursorPosition()
        while position in self.textImmutable:
            position += 1

        if position != self.maxSize:
            self.textbox.setText(
                self.textbox.text()[:position] + str(digit) + self.textbox.text()[position+1:]
            )
            self.textbox.setCursorPosition(position+1)

    @pyqtSlot()
    def del_click(self) -> None:
        position = self.textbox.cursorPosition()
        value = self.textbox.text()
        while position-1 in self.textImmutable:
            position -= 1
        if position != 0:
            self.textbox.setText(value[:position-1] + "0" + value[position:])
            self.textbox.setCursorPosition(position-1)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = MainWindow()

    sys.exit(app.exec_())
