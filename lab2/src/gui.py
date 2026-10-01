import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog, QTableWidget, QTableWidgetItem,
                             QProgressBar, QMessageBox, QHeaderView)
from worker import ScannerThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Metadata Scanner")
        self.resize(1000, 600)
        self.worker = None

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        btn_layout = QHBoxLayout()
        self.btn_select = QPushButton("Выбрать папку")
        self.btn_select.clicked.connect(self.select_folder)
        btn_layout.addWidget(self.btn_select)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        btn_layout.addWidget(self.progress)
        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Имя файла", "Ширина", "Высота", "DPI",
            "Глубина цвета", "Сжатие", "Статус"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            self.start_scan(folder)

    def start_scan(self, folder):
        self.btn_select.setEnabled(False)
        self.table.setRowCount(0)
        self.progress.setValue(0)

        files = []
        for root, _, filenames in os.walk(folder):
            for f in filenames:
                if f.lower().endswith(('.jpg', '.jpeg', '.gif', '.tif', '.tiff', '.bmp', '.png', '.pcx')):
                    files.append(os.path.join(root, f))

        self.progress.setMaximum(len(files) if files else 1)

        self.worker = ScannerThread(files)
        self.worker.result_ready.connect(self.add_row)
        self.worker.progress_update.connect(self.progress.setValue)
        self.worker.finished.connect(self.scan_finished)
        self.worker.start()

    def add_row(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, key in enumerate(["filename", "width", "height", "dpi", "depth", "compression", "status"]):
            self.table.setItem(row, col, QTableWidgetItem(str(data.get(key, "-"))))

    def scan_finished(self):
        self.btn_select.setEnabled(True)
        QMessageBox.information(self, "Готово", "Сканирование завершено.")