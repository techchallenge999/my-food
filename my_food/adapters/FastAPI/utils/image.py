import base64


def bytes_to_base_64(image_byte: bytes):
    return base64.b64encode(image_byte)


def base_64_to_bytes(image_b64: str):
    return base64.b64decode(image_b64)
