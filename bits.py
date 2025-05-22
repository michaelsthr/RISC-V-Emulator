class Bits:
    def __init__(self, size: int, init_val: str = "0"):
        self.size = size
        self.bits: list = ["0"] * size

    def __repr__(self):
        return "Bits()"

    def __str__(self):
        formated_bits = ""
        seperator = " "
        temp_bits = "".join(self.bits)
        step = 8
        for i in range(0, self.size, step):
            formated_bits += temp_bits[i : i + step] + seperator
        return formated_bits

    def set_at_index(self, idx: int, value: str) -> str:
        self.bits[idx] = value

    def set_all(self, value: str):
        self.bits = value.split()

    def get_at_index(self, idx: int) -> str:
        return self.bits[idx]
    
    def get_all(self) -> str:
        return "".joint(self.bits)


if __name__ == "__main__":
    bits = Bits(size=32)
    print(bits)
