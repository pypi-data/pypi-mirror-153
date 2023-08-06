import os
from io import BytesIO

from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase.pdfmetrics import stringWidth

from foledol.django.utils import image_ratio


class ReportColumn:
    def __init__(self, width, label):
        self.width = width
        self.label = label


class ReportItem:
    def __init__(self, key, label, route=None, confirm=False, report=None):
        self.key = key
        self.label = label
        self.route = route
        self.confirm = confirm
        self.report = report


def build_report(builder):
    buffer = BytesIO()
    page = canvas.Canvas(buffer)
    builder(page)

    page.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


class Report:
    line_spacing_small = 10
    line_spacing_normal = 15
    line_spacing_large = 20
    line_padding = 5
    warning = Color(0.9, 0, 0, 0.7)
    list_color = Color(0.9, 0.9, 0.9)
    font_size = 8
    font = 'Helvetica'

    def cut(self, text, font, font_size, width):
        text_width = stringWidth(text, font, font_size)
        while text_width > width:
            text = text[:-1]
            text_width = stringWidth(text, font, font_size)
        return text

    def get_lines(self, text, font, font_size, width):
        words = text.split() if text else []
        lines = []
        line = None
        for word in words:
            new_line = line + " " + word if line else word
            line_width = stringWidth(new_line, font, font_size)
            if line_width < width or line is None:
                line = new_line
            else:
                lines.append(line)
                line = word
        if line is not None and len(line) > 0:
            lines.append(line)
        return lines

    def get_height(self, text, font, font_size, width, line_spacing=line_spacing_normal):
        lines_count = len(self.get_lines(text, font, font_size, width))
        return lines_count * line_spacing if lines_count > 1 else line_spacing

    def wrap(self, page, x, y, text, font, font_size, width, line_spacing=line_spacing_small):
        lines = self.get_lines(text, font, font_size, width)
        for line in lines:
            page.drawString(x, y, self.cut(line, font, font_size, width))
            y -= line_spacing
        return y

    def compute_height(self, columns, values, line_spacing=line_spacing_normal, font=None, font_size=8):
        i = 0
        max_height = 0
        font = font if font else self.font
        for column in columns:
            height = self.get_height(values[i], font, font_size, column.width, line_spacing)
            if height > max_height:
                max_height = height
            i += 1
        return max_height

    def draw_row(self, page, x, y, columns, values, font=None, font_size=8, column_padding=0):
        i = 0
        font = font if font else self.font
        for column in columns:
            self.wrap(page, x, y, values[i], font, font_size, column.width)
            x += column.width
            x += column_padding
            i += 1
        return x

    def draw_row_nowrap(self, page, x, y, columns, values, font=None, font_size=8, column_padding=0):
        i = 0
        font = font if font else self.font
        for column in columns:
            page.drawString(x, y, self.cut(values[i], font, font_size, column.width))
            x += column.width
            x += column_padding
            i += 1
        return x

    def draw_title(self, page, x, y, title):
        path = os.path.join(settings.STATIC_FILES, 'logo.jpeg')
        path_logo = path if os.path.isfile(path) else None
        if path_logo:
            ratio_logo = image_ratio(path_logo)
            page.drawImage(path_logo, x, y - 10, int(32 * ratio_logo), 32)
            x += 55
        page.drawString(x, y, title)


class PredefinedReport:
    def __init__(self, name, filename, label, filter, report):
        self.name = name
        self.filename = filename
        self.label = label
        self.filter = filter
        self.report = report
