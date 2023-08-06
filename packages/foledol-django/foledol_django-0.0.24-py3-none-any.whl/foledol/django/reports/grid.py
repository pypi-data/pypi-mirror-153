from io import BytesIO

from reportlab.lib.pagesizes import landscape, letter

from foledol.django.templatetags.form_extras import value
from foledol.django.tools.canvas import NumberedPageCanvas
from foledol.django.tools.report import Report, ReportColumn


class GridReport(Report):
    def __init__(self, title, grid, fields):
        self.title = title
        self.grid = grid
        self.fields = fields
        self.columns = []
        for column in self.grid.column_set.all().order_by('order'):
            field = self.get_field(column.label)
            if field and not column.hidden:
                width = column.width if column.width and column.width > 0 else 60
                self.columns.append(
                    ReportColumn(width, field.label)
                )

    def get_field(self, key):
        for field in self.fields:
            if field.key == key:
                return field
        return None

    def header(self, page, x, y):
        page.setFont(self.font + '-Bold', 8)
        for column in self.columns:
            page.drawString(x, y, column.label)
            x += column.width

    def build(self, rows):

        buffer = BytesIO()
        page = NumberedPageCanvas(buffer)
        page.setPageSize(landscape(letter))

        y = 580
        page.setFont(self.font + '-Bold', 20)
        page.drawString(10, y, self.title)
        y -= 20

        self.header(page, 20, 560)

        count = 0

        y = 540
        page.setFont(self.font, 8)
        for row in rows:

            values = []
            for column in self.grid.column_set.all():
                field = self.get_field(column.label)
                if field and not column.hidden:
                    values.append(str(row[column.label] if self.grid.group_by else value(row, column.label)))

            i = 0
            max_height = 0
            for column in self.columns:
                height = self.get_height(values[i], self.font, 8, column.width)
                if height > max_height:
                    max_height = height
                i += 1

            if y - max_height < 40:
                page.showPage()
                self.header(page, 20, 580)
                page.setFont(self.font, 8)
                y = 560

            if count % 2 == 0:
                page.setStrokeAlpha(0)
                page.setFillColor(self.list_color)
                page.rect(10, y+self.font_size-max_height, 760, max_height, fill=1)
                page.setFillColorRGB(0, 0, 0, 1)
            count += 1

            x = 20
            i = 0
            for column in self.columns:
                self.wrap(page, x, y, values[i], self.font, 8, column.width)
                x += column.width
                i += 1

            y -= max_height
            y -= self.line_padding

        page.showPage()
        page.save()

        pdf = buffer.getvalue()
        buffer.close()
        return pdf
