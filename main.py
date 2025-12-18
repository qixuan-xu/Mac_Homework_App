import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QLabel, QPushButton,
    QGridLayout, QSpacerItem, QSizePolicy
)



def main():
    app = QApplication([])
    window = QWidget()
    layout = QHBoxLayout()
    window.setFixedSize(800, 600)
    label = QLabel("Hello from my Mac app!")
    button = QPushButton("Click Me!")
    textbox = QLineEdit()
    def on_button_clicked():
        entered_text = textbox.text()
        label.setText(f'Button clicked! You entered: {entered_text}')

    button.clicked.connect(on_button_clicked)
    layout.addWidget(textbox)
    layout.addWidget(label)
    layout.addWidget(button)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()