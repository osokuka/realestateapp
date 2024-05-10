import qrcode
from io import BytesIO
import base64

def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a BytesIO object
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the binary data to base64
    image_base64 = base64.b64encode(image_png)
    return image_base64.decode('utf-8')
    return response