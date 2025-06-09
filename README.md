# RISC-V-Emulator

### Working examples:

| Example | Status |
|---------|--------|
| example_1 | ✓ |
| example_2 | ✓ |
| example_3 | ✓ |
| example_4 | ✓ |
| example_5 | ✓ |
| example_6 | ✓ |
| example_7 | ✓ |
| example_8 | ✓ |
| example_9 | ✓ |

### Implemented instructions:

| Category | Instructions |
|----------|-------------|
| **Arithmetic** | `add`, `addi`, `sub`, `slt` |
| **Bitwise Logic** | `and`, `andi`, `or`, `ori`, `xor` |
| **Load Immediate** | `li`, `lui`, `auipc` |
| **Branch** | `beq`, `bne` |
| **Jump and Function** | `j`, `jal`, `jalr` |
| **Load and Store** | `lw`, `sw` |


### Known bugs:
- If the editor wraps the text, blocks not parsed well
- \n are not recognized
- offset not working properly (should be multiple of 4)