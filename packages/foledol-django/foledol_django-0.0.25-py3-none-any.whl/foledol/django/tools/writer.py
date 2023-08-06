import io
import xlsxwriter
from django.http import HttpResponse


class WriterColumn:
    def __init__(self, title, size=None):
        self.title = title
        self.size = size


class WriterCell:
    def __init__(self, value, cell_format=None):
        self.value = value
        self.cell_format = cell_format


class Writer:
    cell_format = None
    wrap_format = None
    date_format = None
    hour_format = None
    currency_format = None

    def __init__(self, title, columns=None):
        self.output = io.BytesIO()

        self.workbook = xlsxwriter.Workbook(self.output, {'in_memory': True, 'remove_timezone': True})

        header_format = self.workbook.add_format()
        header_format.set_bold(True)
        header_format.set_align('top')
        header_format.set_align('center')
        header_format.set_text_wrap(True)

        self.cell_format = self.workbook.add_format()
        self.cell_format.set_align('top')
        self.wrap_format = self.workbook.add_format()
        self.wrap_format.set_text_wrap(True)

        self.date_format = self.workbook.add_format({'num_format': 'dd-mm-yy'})
        self.hour_format = self.workbook.add_format({'num_format': 'hh:mm'})
        self.currency_format = self.workbook.add_format({'num_format': '#,##0.00'})

        self.worksheet = self.workbook.add_worksheet(title)
        self.worksheet.set_landscape()

        if columns:
            index = 0
            for column in columns:
                self.worksheet.write(0, index, column.title, header_format)
                if column.size:
                    self.worksheet.set_column(index, index, column.size)
                index += 1

        self.row = 1

    def write(self, cells):
        index = 0
        for cell in cells:
            if cell:
                if cell.cell_format:
                    self.worksheet.write(self.row, index, cell.value, cell.cell_format)
                else:
                    self.worksheet.write(self.row, index, cell.value)
            index += 1
        self.row += 1

    def save(self, filename):
        self.workbook.close()
        self.output.seek(0)
        response = HttpResponse(
            self.output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
        return response
