from model import ColorMath

class ColorController:
    def __init__(self):
        self.r, self.g, self.b = 0, 0, 0
        self.cmyk_method = "GCR"
        self.view = None

    def set_view(self, view):
        self.view = view
        self.update_all()

    def set_cmyk_method(self, method):
        self.cmyk_method = method
        self.update_all()

    def ui_changed(self, model_name, channel, value, pick=None):
        if pick:
            self.r, self.g, self.b = pick.red(), pick.green(), pick.blue()
            self.update_all()
            return

        if model_name == "RGB":
            if channel == "R": self.r = value
            elif channel == "G": self.g = value
            elif channel == "B": self.b = value

        elif model_name == "HSV":
            h = value if channel == "H" else self.view.spins["HSV_H"].value()
            s = value if channel == "S" else self.view.spins["HSV_S"].value()
            v = value if channel == "V" else self.view.spins["HSV_V"].value()
            self.r, self.g, self.b = ColorMath.hsv_to_rgb(h, s, v)

        elif model_name == "CMYK":
            c = value if channel == "C" else self.view.spins["CMYK_C"].value()
            m = value if channel == "M" else self.view.spins["CMYK_M"].value()
            y = value if channel == "Y" else self.view.spins["CMYK_Y"].value()
            k = value if channel == "K" else self.view.spins["CMYK_K"].value()
            self.r, self.g, self.b = ColorMath.cmyk_to_rgb(c, m, y, k)

        self.r = max(0, min(255, round(self.r)))
        self.g = max(0, min(255, round(self.g)))
        self.b = max(0, min(255, round(self.b)))

        self.update_all()

    def update_all(self):
        h, s, v = ColorMath.rgb_to_hsv(self.r, self.g, self.b)
        c, m, y, k = ColorMath.rgb_to_cmyk(self.r, self.g, self.b, self.cmyk_method)

        values = {
            "RGB_R": self.r, "RGB_G": self.g, "RGB_B": self.b,
            "HSV_H": h, "HSV_S": s, "HSV_V": v,
            "CMYK_C": c, "CMYK_M": m, "CMYK_Y": y, "CMYK_K": k
        }
        self.view.update_ui_values(values)