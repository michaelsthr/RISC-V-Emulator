class Word:
    def __init__(self, dez: int = 0, size: int = 32):
        self.size = size

        self.base10: str = dez
        self.base2: str = format(dez, "b").zfill(self.size)
        self.base16: str = format(dez, "x").zfill(self.size // 4)

    def __repr__(self):
        return f"BinaryWord(base10_val={self.base10}, base2_val={self.base2}, base16_val={self.base16}, size={self.size})"

    def __str__(self) -> str:
        step = 8
        return " ".join(
            self.base2[i : i + step] for i in range(0, len(self.base2), step)
        )

    def __add__(self, word: "Word") -> "Word":
        res_base10 = self.base10 + word.base10
        return Word(dez=res_base10)

    def __sub__(self, word: "Word") -> "Word":
        res_base10 = self.base10 - word.base10
        return Word(dez=res_base10)

    def __and__(self, word: "Word") -> "Word":
        res_base10 = self.base10 & word.base10
        return Word(dez=res_base10)

    def __or__(self, word: "Word") -> "Word":
        res_base10 = self.base10 | word.base10
        return Word(dez=res_base10)

    def __xor__(self, word: "Word") -> "Word":
        res_base10 = self.base10 ^ word.base10
        return Word(dez=res_base10)
    
    def __eq__(self, word: "Word") -> bool:
        return self.base10 == word.base10
    
    def __ne__(self, word: "Word") -> bool:
        return self.base10 != word.base10
    
    def __lt__(self, word: "Word") -> bool:
        return self.base10 < word.base10
    
    def __lshift__(self, word: "Word") -> "Word":
        res_base10 = self.base10 << word.base10
        return Word(res_base10)

    def set_bit_at_index(self, idx: int, value: str) -> str:
        self.bits[idx] = value

    def set_by_dez(self, dez_val: int):
        self.base10 = dez_val
        self.base2 = format(dez_val, "b").zfill(self.size)
        self.hez_ = format(dez_val, "x").zfill(self.size // 4)

    def set_by_bin(self, bin_val: str):
        self.base2 = bin_val
        self.base10 = int(bin_val, 2)
        self.base16 = format(int(bin_val, 2), "x").zfill(self.size // 4)

    def set_by_hex(self, hex_val: str):
        self.base16 = hex_val
        self.base10 = int(hex_val, 16)
        self.base2 = format(int(hex_val, 16), "b").zfill(self.size)

    @property
    def bin(self) -> str:
        return self.base2

    @property
    def dez(self) -> int:
        return self.base10

    @property
    def hex(self) -> str:
        return self.base16
