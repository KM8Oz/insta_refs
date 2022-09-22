from io import BytesIO
import io
from PIL import Image
import requests

class random_image:
    def __init__(self) -> None:
        pass
    def get_image(w,h):
        response = requests.get(f"https://picsum.photos/{w}/{h}")
        img = Image.open(BytesIO(response.content))
        b = io.BytesIO()
        img.save(b, 'jpeg')
        im_bytes = b.getvalue()
        return im_bytes