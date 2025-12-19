import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)


class DraggableWindow(QWidget):
    """Main window that can be dragged from anywhere."""

    def __init__(self):
        super().__init__()
        self._drag_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self._drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = None
            event.accept()
        super().mouseReleaseEvent(event)


def main():
    app = QApplication([])
    window = DraggableWindow()

    # 允许改大小（初始 + 最小）
    window.resize(800, 600)
    window.setMinimumSize(420, 240)

    # ===== 1) 顶部：标题区（水平布局）=====
    title = QLabel("Mac Homework App")
    title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    title.setStyleSheet("font-size: 20px; font-weight: 600;")  # 简单让标题更像 App

    # 如果你以后想在标题右侧加一个状态/图标，这里就是位置
    top_bar = QHBoxLayout()
    top_bar.addWidget(title)
    top_bar.addStretch()  # 把右侧顶开（右边留空）

    # ===== 2) 中间：输入区（垂直布局）=====
    prompt = QLabel("请输入内容：")
    textbox = QLineEdit()
    textbox.setPlaceholderText("在这里输入…")

    middle = QVBoxLayout()
    middle.addWidget(prompt)
    middle.addWidget(textbox)

    # ===== 3) 中间：文本  =====
    middle_text = QLabel("这里是中间说明文字，可以写提示、说明或状态信息。")
    middle_text.setWordWrap(True)
    middle_text.setContentsMargins(16, 0, 16, 0)  # 文字和边框的内边距
    middle_text.setFixedHeight(100)  # 胶囊高度（你可改 48/56/64）

    middle_box = QFrame()
    middle_box.setAttribute(Qt.WA_StyledBackground, True)  # ⭐ 让 QFrame 按样式画背景
    middle_box.setFrameShape(QFrame.NoFrame)  # ⭐ 避免系统再画框
    middle_box.setFrameShadow(QFrame.Plain)


    middle_box.setStyleSheet("""
        QFrame {
            border: 2px solid #93C5FD;
            border-radius: 16px;
            background: transparent;
        }
    """)

    middle_text.setStyleSheet("""
        QLabel {
            background-color: rgba(239, 246, 255, 0.12);
            
            border-radius: 12px;
        }
    """)#color: #000000;

    box_layout = QVBoxLayout(middle_box)
    box_layout.setContentsMargins(0,0,0,0)
    box_layout.addWidget(middle_text)

    # ===== 4) 底部：按钮栏（水平布局，按钮靠右）=====
    label = QLabel("Hello from my Mac app!")
    label.setWordWrap(True)  # 文本长了自动换行（更像 App）

    button = QPushButton("Submit")

    def on_button_clicked():
        entered_text = textbox.text().strip()
        if not entered_text:
            middle_text.setText("你还没输入内容。")
        else:
            middle_text.setText(f"已提交：{entered_text}")

    button.clicked.connect(on_button_clicked)

    bottom_bar = QHBoxLayout()
    bottom_bar.addWidget(label)     # 左侧信息区
    bottom_bar.addStretch()         # 把按钮推到右边
    bottom_bar.addWidget(button)    # 右侧按钮

    # ===== 总布局：垂直（上-中-下）=====
    root = QVBoxLayout()
    root.setContentsMargins(30, 20, 30, 20)  # 内边距（更像 App）
    root.setSpacing(12)                      # 控件间距


    root.addLayout(top_bar)
    root.addLayout(middle)
    root.addSpacing(10)
    #root.addWidget(middle_text)  # 中间的“文字说明”
    root.addWidget(middle_box)
    root.addStretch()
    root.addLayout(bottom_bar)

    window.setLayout(root)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
