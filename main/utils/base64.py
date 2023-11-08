import base64

def enc_base64(str):
    encoded_str = base64.b64encode(str.encode('ascii'))
    encoded_ascii_str = encoded_str.decode('ascii')

    return encoded_ascii_str


def dec_base64(str):
    decoded_str = base64.b64decode(str.encode('ascii'))
    decoded_ascii_str = decoded_str.decode('ascii')

    return decoded_ascii_str