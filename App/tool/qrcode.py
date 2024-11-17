import qrcode
from io import BytesIO
from flask import send_file
from werkzeug.wrappers import Response


def str_to_qrcode(txt: str) -> Response:
    qr = qrcode.make("hello world")
    img_io = BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


__all__ = ["str_to_qrcode"]
