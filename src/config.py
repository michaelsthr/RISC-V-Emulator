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
    "beq_taken": 2,
    "beq_not_taken": 1,
    "bne_taken": 2,
    "bne_not_taken": 1,
    "jal": 2,
    "j": 1,
    "jalr": 2,
    "slt": 1,
    "lui": 1,
    "auipc": 1,
    "lw": 2,
    "sw": 2,
    "ecall": 1,
    "ebreak": 1,
}

# UNIT: GHZ
FREQUENCY: float = 4.0

EXAMPLE_FILES = [
    "example_1.s",
    "example_2.s",
    "example_3.s",
    "example_4.s",
    "example_5.s",
    "example_6.s",
    "example_7.s",
    "example_8.s",
    "example_9.s",
]
