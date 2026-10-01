from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QSlider, QSpinBox, QComboBox, QPushButton, QColorDialog)
from PyQt6.QtCore import Qt


class ColorView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Color Converter (RGB ↔ CMYK ↔ HSV)")
        self.setGeometry(100, 100, 650, 350)

        self.sliders = {}
        self.spins = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        settings_layout = QHBoxLayout()
        self.cmyk_method_combo = QComboBox()
        self.cmyk_method_combo.addItems(["GCR", "UCR"])
        self.cmyk_method_combo.currentTextChanged.connect(self.controller.set_cmyk_method)
        settings_layout.addWidget(QLabel("Алгоритм цветоделения CMYK:"))
        settings_layout.addWidget(self.cmyk_method_combo)
        settings_layout.addStretch()
        main_layout.addLayout(settings_layout)

        top_layout = QHBoxLayout()
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(100, 100)
        self.color_preview.setStyleSheet("background-color: rgb(0,0,0); border: 1px solid black;")

        self.btn_pick = QPushButton("Палитра (ОС)")
        self.btn_pick.clicked.connect(self.pick_color)

        top_layout.addWidget(self.color_preview)
        top_layout.addWidget(self.btn_pick)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)

        grid = QGridLayout()
        self.add_model_controls(grid, "RGB", ["R", "G", "B"], 255, 0)
        self.add_model_controls(grid, "CMYK", ["C", "M", "Y", "K"], 100, 1)
        self.add_model_controls(grid, "HSV", ["H", "S", "V"], [360, 100, 100], 2)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def add_model_controls(self, grid, model_name, channels, max_vals, col_offset):
        grid.addWidget(QLabel(f"<b>{model_name}</b>"), 0, col_offset * 3)
        for i, ch in enumerate(channels):
            lbl = QLabel(ch)
            sl = QSlider(Qt.Orientation.Horizontal)
            sp = QSpinBox()

            m_val = max_vals[i] if isinstance(max_vals, list) else max_vals
            sl.setMaximum(m_val)
            sp.setMaximum(m_val)

            sl.valueChanged.connect(lambda val, c=ch, m=model_name: self.controller.ui_changed(m, c, val))
            sp.valueChanged.connect(lambda val, c=ch, m=model_name: self.controller.ui_changed(m, c, val))

            self.sliders[f"{model_name}_{ch}"] = sl
            self.spins[f"{model_name}_{ch}"] = sp

            grid.addWidget(lbl, i + 1, col_offset * 3)
            grid.addWidget(sl, i + 1, col_offset * 3 + 1)
            grid.addWidget(sp, i + 1, col_offset * 3 + 2)

    def block_all_signals(self, block):
        for sl in self.sliders.values(): sl.blockSignals(block)
        for sp in self.spins.values(): sp.blockSignals(block)

    def update_ui_values(self, values_dict):
        self.block_all_signals(True)
        for key, val in values_dict.items():
            if key in self.sliders:
                self.sliders[key].setValue(int(val))
                self.spins[key].setValue(int(val))
        self.block_all_signals(False)

        r, g, b = values_dict["RGB_R"], values_dict["RGB_G"], values_dict["RGB_B"]
        self.color_preview.setStyleSheet(f"background-color: rgb({int(r)},{int(g)},{int(b)}); border: 1px solid black;")
        self.update_gradients(int(r), int(g), int(b))

    def update_gradients(self, r, g, b):
        self.set_slider_style(self.sliders["RGB_R"], f"rgb(0,{g},{b})", f"rgb(255,{g},{b})")
        self.set_slider_style(self.sliders["RGB_G"], f"rgb({r},0,{b})", f"rgb({r},255,{b})")
        self.set_slider_style(self.sliders["RGB_B"], f"rgb({r},{g},0)", f"rgb({r},{g},255)")
        self.set_slider_style(self.sliders["HSV_V"], "black", f"rgb({r},{g},{b})")

    def set_slider_style(self, slider, color_start, color_end):
        style = f"""
        QSlider::groove:horizontal {{
            height: 12px; border-radius: 6px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {color_start}, stop:1 {color_end});
        }}
        QSlider::handle:horizontal {{
            background: white; border: 2px solid gray;
            width: 14px; margin: -2px 0; border-radius: 7px;
        }}
        """
        slider.setStyleSheet(style)

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.controller.ui_changed("RGB", "R", color.red(), pick=color)