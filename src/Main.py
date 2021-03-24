from PyQt6.QtWidgets import QApplication
from Scene import Scene


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Scene()
    window.show()
    sys.exit(app.exec())