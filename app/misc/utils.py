from io import BytesIO
import qrcode
from base64 import b64encode

def generate_qr_code(data: str) -> str:
    """Generates a QR code for the given data and returns it as a base64-encoded string."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered)
    img_str = b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"