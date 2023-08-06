from datetime import datetime

import pytz
from reportlab.pdfgen.canvas import Canvas


class NumberedPageCanvas(Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    http://www.blog.pythonlibrary.org/2013/08/12/reportlab-how-to-add-page-numbers/
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []
        self.bookmarks = {}

    def closePage(self):
        self.pages.append(dict(self.__dict__))

    def showPage(self):
        self.closePage()
        self._startPage()

    def save(self):
        page_count = len(self.pages)

        date = datetime.utcnow().astimezone(pytz.timezone("Europe/Paris")).strftime('%d/%m/%Y %H:%M')

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count, date)
            super().showPage()

        super().save()

    def presetBookmarkPage(self, key):
        if self._pageNumber in self.bookmarks:
            self.bookmarks[self._pageNumber].append(key)
        else:
            self.bookmarks[self._pageNumber] = [key]

    def draw_page_number(self, page_count, date):
        page = "Page %s sur %s" % (self._pageNumber, page_count)
        if self._pageNumber in self.bookmarks:
            for key in self.bookmarks[self._pageNumber]:
                self.bookmarkPage(key)
        self.setFont("Helvetica", 9)
        self.drawString(30, 30, date)
        self.drawRightString(self._pagesize[0]-80, 30, page)
        #self.drawRightString(179 * mm, -280 * mm, page)