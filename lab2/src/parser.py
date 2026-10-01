import struct
import os

def parse_image(filepath):
    size = os.path.getsize(filepath)
    with open(filepath, 'rb') as f:
        header = f.read(32)
        if not header:
            return {"status": "Файл пуст"}

        if header.startswith(b'\x89PNG\r\n\x1a\n'):
            return _parse_png(f, size)
        elif header.startswith(b'\xff\xd8'):
            return _parse_jpg(f, size)
        elif header.startswith(b'BM'):
            return _parse_bmp(f, header)
        elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
            return _parse_gif(header)
        elif header.startswith(b'\x0a'):
            return _parse_pcx(header)
        elif header.startswith(b'II*\x00') or header.startswith(b'MM\x00*'):
            return _parse_tif(f, header)
        else:
            return {"status": "Подмена расширения"}

def _parse_png(f, size):
    meta = {"status": "ОК", "compression": "Deflate"}
    f.seek(8)
    while True:
        chunk_header = f.read(8)
        if len(chunk_header) < 8:
            meta["status"] = "Поврежден (нет IEND)"
            break
        length, chunk_type = struct.unpack(">I4s", chunk_header)
        if chunk_type == b'IHDR':
            data = f.read(length)
            w, h, depth = struct.unpack(">IIB", data[:9])
            meta["width"] = w
            meta["height"] = h
            meta["depth"] = depth
            f.seek(4, 1)
        elif chunk_type == b'pHYs':
            data = f.read(length)
            ppu_x, ppu_y, unit = struct.unpack(">IIB", data)
            if unit == 1:
                meta["dpi"] = round(ppu_x * 0.0254)
            f.seek(4, 1)
        elif chunk_type == b'IEND':
            break
        else:
            f.seek(length + 4, 1)
    return meta

def _parse_jpg(f, size):
    meta = {"status": "ОК", "compression": "JPEG"}
    f.seek(-2, 2)
    eoi = f.read(2)
    if eoi != b'\xff\xd9':
        meta["status"] = "Поврежден (нет EOI)"
    f.seek(2)
    while True:
        marker = f.read(2)
        if not marker or len(marker) < 2:
            break
        if marker[0] != 0xff:
            break
        if marker[1] in (0xc0, 0xc2):
            f.seek(3, 1)
            h, w = struct.unpack(">HH", f.read(4))
            meta["width"] = w
            meta["height"] = h
            meta["depth"] = 24
            break
        else:
            length = struct.unpack(">H", f.read(2))[0]
            f.seek(length - 2, 1)
    return meta

def _parse_bmp(f, header):
    meta = {"status": "ОК"}
    w, h, planes, depth, comp = struct.unpack("<IIHHH", header[18:34])
    meta["width"] = w
    meta["height"] = h
    meta["depth"] = depth
    comp_dict = {0: "BI_RGB", 1: "BI_RLE8", 2: "BI_RLE4"}
    meta["compression"] = comp_dict.get(comp, str(comp))
    return meta

def _parse_gif(header):
    meta = {"status": "ОК", "compression": "LZW"}
    w, h = struct.unpack("<HH", header[6:10])
    packed = header[10]
    depth = ((packed & 0x70) >> 4) + 1
    meta["width"] = w
    meta["height"] = h
    meta["depth"] = depth
    return meta

def _parse_pcx(header):
    meta = {"status": "ОК", "compression": "RLE"}
    xmin, ymin, xmax, ymax = struct.unpack("<HHHH", header[4:12])
    meta["width"] = xmax - xmin + 1
    meta["height"] = ymax - ymin + 1
    meta["depth"] = header[3] * header[65]
    return meta

def _parse_tif(f, header):
    meta = {"status": "ОК"}
    byte_order = ">" if header[:2] == b'MM' else "<"
    offset = struct.unpack(byte_order + "I", header[4:8])[0]
    f.seek(offset)
    num_tags = struct.unpack(byte_order + "H", f.read(2))[0]
    for _ in range(num_tags):
        tag, dtype, count, value = struct.unpack(byte_order + "HHII", f.read(12))
        if tag == 256:
            meta["width"] = value
        elif tag == 257:
            meta["height"] = value
        elif tag == 258:
            meta["depth"] = value
        elif tag == 259:
            meta["compression"] = value
    return meta