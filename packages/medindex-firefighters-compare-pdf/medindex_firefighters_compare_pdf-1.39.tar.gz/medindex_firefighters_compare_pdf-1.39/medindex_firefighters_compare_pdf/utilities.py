import base64


def save(file_path, binary_content):
    data = base64.b64decode(binary_content)
    with open(file_path, 'wb') as out_file:
        out_file.write(data)


def read_file(filepath):
    with open(filepath, 'rb') as file:
        return file.read()
