import re

LABEL_REGEX: str = re.compile(
    r"^[a-zA-Z_][a-zA-Z0-9_]*:$" # (sum:, end:, ...)
)

INSTRUCTION_REGEX: str = re.compile(
    r"^\s*"                      # Begin, optional space
    r"([a-z]+)"                  # Opcode (addi, beq, ...)
    r"\s+"                       # Space
    r"([x]\d+|\w+)"              # 1. operand
    r"(?:\s*,\s*([x]\d+|\w+))?"  # 2. operand (optional)
    r"(?:\s*,\s*([x]\d+|\w+))?"  # 3. operand (optional)
    r"\s*(?:#.*)?$"              # comment (otional)
)

