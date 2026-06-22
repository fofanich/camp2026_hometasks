import cv2
import numpy as np
from pathlib import Path

HERE = Path(__file__).parent

# Load both models once at startup and keep them in a dictionary {scale: model}
_models = {}
for scale in (2, 4):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(str(HERE / f"FSRCNN_x{scale}.pb"))
    sr.setModel("fsrcnn", scale)
    _models[scale] = sr


def upscale_image(image_bytes: bytes, scale: int = 2) -> bytes:
    if scale not in _models: # only 2 and 4 are allowed
        raise ValueError("scale must be 2 or 4")

    array = np.frombuffer(image_bytes, dtype=np.uint8) # bytes -> array of numbers
    image = cv2.imdecode(array, cv2.IMREAD_COLOR) # array -> OpenCV image

    if image is None: # not bytes of an image
        raise ValueError("not an image")

    result = _models[scale].upsample(image) # the actual upscaling (x2 or x4)

    ok, encoded = cv2.imencode(".png", result) # image -> PNG bytes
    return encoded.tobytes()