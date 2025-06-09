CPI_VALUES = {
    "add": 1,
    "sub": 1,
    "and": 1,
    "or": 1,
    "xor": 1,
    "addi": 1,
    "andi": 1,
    "ori": 1,
    "li": 1,
    "beqtaken": 2,
    "beqnotaken": 1,
    "bnetaken": 2,
    "bnenotaken": 1,
    "jal": 2,
    "j": 1,
    "jalr": 2,
    "lui": 1,
    "auipc": 1,
    "lw": 2,
    "sw": 2,
    "ecall": 1,
    "ebreak": 1,
}

# UNIT: GHZ
FREQUENCY: float = 4.0