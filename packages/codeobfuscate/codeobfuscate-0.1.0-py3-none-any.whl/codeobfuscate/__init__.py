"""
Usage: create new file, write:
from obfuscate import Encode

Encode('C://to_ofuscate.py') # file name
dont obfuscate in main file its bad for module.
Good:
main.py:
    class A:
        def __init__(self) -> None:
            print("A init")

        def __call__(self, *args, **kwds):
            print("call to A")

    class B(A):
        def __init__(self) -> None:
            super().__init__()
            print("B init")
        def __call__(self, *args, **kwds):
            return super().__call__(*args, **kwds)

    b = B()
    print(b())
    
obf.py:
    from obfuscate import Encode

    Encode('main.py')

"""
from .load import Load
import base64


class Encode:
    def __init__(self, file: str):
        with open(file, "r", encoding="utf-8") as f:
            self.code = f.read()
        self.file = file
        self.encode()

    def encode(self):
        code_list = self.code.split("\n")
        new_code_list = []
        for line in code_list:
            if line != "":
                new_code_list.append(base64.b64encode(line.encode("utf-8")))
        self.code = "# pyobfuscate executed. dont remove this\nfrom pyobfuscate import Load\n\nLoad(\""
        for data in new_code_list:
            data = bytes(data).decode("utf-8")
            self.code += f"{data}|"
        self.code += "\")\n"
        with open(self.file, "w") as f:
            f.write(self.code)


if __name__ == "__main__":
    Encode(__file__)
