import sys
from PyQt6.QtWidgets import QApplication
from controller import ColorController
from view import ColorView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = ColorController()
    view = ColorView(controller)
    controller.set_view(view)

    view.show()
    sys.exit(app.exec())