import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt

class MyMainWindow(QMainWindow):
    def closeEvent(self, event):
        # Hiển thị hộp thoại xác nhận trước khi đóng cửa sổ
        reply = QMessageBox.question(self, 'Xác nhận', 'Bạn có chắc muốn đóng cửa sổ?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Đồng ý đóng cửa sổ
            event.accept()
        else:
            # Ngăn không cho đóng cửa sổ
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.setWindowTitle('Xử lý sự kiện "close" trong PyQt5')
    window.setGeometry(100, 100, 400, 300)
    window.show()
    sys.exit(app.exec_())
