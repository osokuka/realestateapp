import qrcode
from io import BytesIO
from django.http import HttpResponse

def generate_qr(request, data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response
