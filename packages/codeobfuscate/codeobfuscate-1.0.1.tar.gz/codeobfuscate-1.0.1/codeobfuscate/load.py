import base64


class Load:
    def __init__(self, value):
        self.bytes = value.split("|")
        self.code = ""
        self.decode()

    def decode(self):
        for b in self.bytes:
            code = base64.b64decode(str(b).encode("utf-8")).decode("utf-8")
            self.code += code
            self.code += "\n"
        exec(self.code)
