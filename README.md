# RISC-V-Emulator

![alt text](res/screenshot.png)

## Setup

Follow these steps to set up and run the RISC-V emulator on your machine.

### Prerequisites

- Python 3.10 or newer
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/michaelsthr/RISC-V-Emulator.git
cd RISC-V-Emulator

# Create and activate a virtual environment
python3 -m venv venv        # Create virtual environment
source venv/bin/activate    # Activate (macOS/Linux)

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Run the emulator
python main.py
```

1. Click the *Examples* menu in the top bar to load built-in ASM examples, or select *File* to open your own assembly files (loaded files are copies; originals remain unchanged)
2. Click *Run & Debug* to start the emulator
3. Choose *Execute Step* to execute the current instruction one at a time, or *Execute All* to run the entire program
4. Enjoy exploring my RISC-V emulator ;)

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
| **answer_to_life** | ✓ |

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
- doesnt stop if err in asm