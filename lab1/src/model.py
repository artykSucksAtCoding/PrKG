
class ColorMath:

    @staticmethod
    def rgb_to_hsv(r, g, b):
        r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
        cmax, cmin = max(r_norm, g_norm, b_norm), min(r_norm, g_norm, b_norm)
        delta = cmax - cmin

        v = cmax
        s = 0.0 if cmax == 0 else delta / cmax

        if delta == 0:
            h = 0.0
        elif cmax == r_norm:
            h = 60 * (((g_norm - b_norm) / delta) % 6)
        elif cmax == g_norm:
            h = 60 * (((b_norm - r_norm) / delta) + 2)
        else:
            h = 60 * (((r_norm - g_norm) / delta) + 4)

        return h, s * 100.0, v * 100.0

    @staticmethod
    def hsv_to_rgb(h, s, v):
        s_norm, v_norm = s / 100.0, v / 100.0
        c = v_norm * s_norm
        x = c * (1 - abs((h / 60.0) % 2 - 1))
        m = v_norm - c

        if 0 <= h < 60:
            r_p, g_p, b_p = c, x, 0
        elif 60 <= h < 120:
            r_p, g_p, b_p = x, c, 0
        elif 120 <= h < 180:
            r_p, g_p, b_p = 0, c, x
        elif 180 <= h < 240:
            r_p, g_p, b_p = 0, x, c
        elif 240 <= h < 300:
            r_p, g_p, b_p = x, 0, c
        else:
            r_p, g_p, b_p = c, 0, x

        return (r_p + m) * 255.0, (g_p + m) * 255.0, (b_p + m) * 255.0

    @staticmethod
    def rgb_to_cmyk(r, g, b, method="GCR"):
        c = 1.0 - (r / 255.0)
        m = 1.0 - (g / 255.0)
        y = 1.0 - (b / 255.0)
        k = min(c, m, y)

        if k == 1.0:
            return 0.0, 0.0, 0.0, 100.0

        if method == "GCR":
            c_out = (c - k) / (1.0 - k)
            m_out = (m - k) / (1.0 - k)
            y_out = (y - k) / (1.0 - k)
            k_out = k
        elif method == "UCR":
            threshold = 0.5
            k_ucr = min(1.0, max(0.0, (k - threshold) * 2.0))
            c_out = max(0.0, c - k_ucr)
            m_out = max(0.0, m - k_ucr)
            y_out = max(0.0, y - k_ucr)
            k_out = k_ucr
        else:
            c_out, m_out, y_out, k_out = c, m, y, k

        return c_out * 100.0, m_out * 100.0, y_out * 100.0, k_out * 100.0

    @staticmethod
    def cmyk_to_rgb(c, m, y, k):
        c_norm, m_norm, y_norm, k_norm = c / 100.0, m / 100.0, y / 100.0, k / 100.0
        r = 255.0 * (1.0 - c_norm) * (1.0 - k_norm)
        g = 255.0 * (1.0 - m_norm) * (1.0 - k_norm)
        b = 255.0 * (1.0 - y_norm) * (1.0 - k_norm)
        return r, g, b