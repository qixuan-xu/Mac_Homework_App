import sys  # 用于程序退出（sys.exit）
from PySide6.QtCore import Qt  # Qt 的核心枚举（比如鼠标按键）
from PySide6.QtWidgets import (
    QApplication,  # 整个 Qt 应用的入口
    QWidget,       # 窗口基类
    QLineEdit,     # 文本输入框
    QLabel,        # 文本标签
    QPushButton,   # 按钮
    QHBoxLayout,   # 水平布局
)


class DraggableWindow(QWidget):
    """
    可拖拽的主窗口
    —— 鼠标按住窗口任意位置即可拖动
    """

    def __init__(self):
        super().__init__()
        self._drag_pos = None  # 记录鼠标按下时的位置，用于计算拖动距离

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:  # 判断是否为鼠标左键
            # 记录鼠标全局位置 与 窗口左上角的偏移量
            self._drag_pos = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )
            event.accept()  # 告诉 Qt 这个事件已处理
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """鼠标移动事件（用于拖动窗口）"""
        if event.buttons() & Qt.LeftButton and self._drag_pos is not None:
            # 根据当前鼠标位置减去偏移量，移动窗口
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self._drag_pos = None  # 清空拖动状态
            event.accept()
        super().mouseReleaseEvent(event)


def main():
    """程序主入口"""
    app = QApplication([])  # 创建 Qt 应用
    window = DraggableWindow()  # 创建主窗口

    layout = QHBoxLayout()  # 创建水平布局
    window.setFixedSize(800, 600)  # 固定窗口大小

    label = QLabel("Hello from my Mac app!")  # 显示文本
    button = QPushButton("Click Me!")         # 按钮
    textbox = QLineEdit()                     # 输入框

    def on_button_clicked():
        """按钮点击后的回调函数"""
        entered_text = textbox.text()  # 获取输入框内容
        label.setText(
            f'Button clicked! You entered: {entered_text}'
        )  # 更新标签文本

    button.clicked.connect(on_button_clicked)  # 绑定按钮点击事件

    # 将控件加入布局（从左到右）
    layout.addWidget(textbox)
    layout.addWidget(label)
    layout.addWidget(button)

    window.setLayout(layout)  # 设置窗口布局
    window.show()             # 显示窗口

    sys.exit(app.exec())      # 启动事件循环并安全退出


# 只有直接运行该文件时才执行 main()
if __name__ == '__main__':
    main()
