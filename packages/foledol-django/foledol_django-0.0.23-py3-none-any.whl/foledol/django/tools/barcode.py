import os

import barcode
from PIL import Image
from barcode.writer import ImageWriter
from django.conf import settings

from ..utils import remove_file


class BarCode:

    def __init__(self, uid, value):
        path = os.path.join(settings.MEDIA_ROOT, 'bc39', uid.replace('/', '-'))
        self.path_bc = path + '.png'
        remove_file(self.path_bc)

        bc39 = barcode.get('code39', value, writer=ImageWriter(), options={'add_checksum': False})
        bc39.save(path, {"module_width": 0.3})

        bc39 = Image.open(self.path_bc)
        w, h = bc39.size
        bc39 = bc39.crop((0, 0, w, h - 110))
        bc39_rotated = bc39.rotate(-90, expand=True)
        self.path_bc_rotated = path + "_rotated.png"
        bc39_rotated.save(self.path_bc_rotated)

    def remove(self):
        remove_file(self.path_bc)
        remove_file(self.path_bc_rotated)


def create_bc39(uid, value):
    return BarCode(uid, value) if uid and value else None
