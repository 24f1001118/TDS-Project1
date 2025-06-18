import base64
from io import BytesIO
from PIL import Image
import pytesseract

def process_image_text(image_b64: str) -> str:
    try:
        image_data = base64.b64decode(image_b64)
        image = Image.open(BytesIO(image_data))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"[Error processing image: {str(e)}]"

