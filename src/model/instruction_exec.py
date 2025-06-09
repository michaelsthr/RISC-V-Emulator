from typing import TYPE_CHECKING
from loguru import logger

from .word import Word
from src.config import CPI_VALUES

if TYPE_CHECKING:
    from .cpu import CPU


class InstructionExec:
    def __init__(self, cpu: "CPU"):
        self.cpu = cpu

    def _get_register_index(self, r: str) -> int:
        return self.cpu.get_register_index(r)

    def _get_imm(self, imm: str) -> int:
        return self.cpu.get_imm(imm)

    def _increment_pc(self, amount: int = 4):
        self.cpu.increment_pc(amount)

    def _get_pc(self):
        return self.cpu.get_pc()

    def _set_pc(self, value: int):
        return self.cpu.set_pc(value)

    def _get_base_offset(self, base_offset: str):
        return self.cpu.get_base_offset(base_offset)

    def _increment_clock(self, amount: int):
        self.cpu.increment_clock(amount)

    # --- INSTRUCTIONS ---

    def _add(self, rd: str, rs1: str, rs2: str):
        cpi = CPI_VALUES["add"]

        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)

        self.cpu.register_set[rd] = (
            self.cpu.register_set[rs1] + self.cpu.register_set[rs2]
        )
        self._increment_pc()
        self._increment_clock(cpi)
        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd].base10}")

    def _sub(self, rd: str, rs1: str, rs2: str):
        cpi = CPI_VALUES["sub"]
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)

        self.cpu.register_set[rd] = (
            self.cpu.register_set[rs1] - self.cpu.register_set[rs2]
        )
        self._increment_pc()
        self._increment_clock(cpi)
        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd].base10}")

    def _and(self, rd: str, rs1: str, rs2: str):
        cpi = CPI_VALUES["and"]
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)

        self.cpu.register_set[rd] = (
            self.cpu.register_set[rs1] & self.cpu.register_set[rs2]
        )
        self._increment_pc()
        self._increment_clock(cpi)
        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd].base10}")

    def _or(self, rd: str, rs1: str, rs2: str):
        cpi = CPI_VALUES["or"]
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)

        self.cpu.register_set[rd] = (
            self.cpu.register_set[rs1] | self.cpu.register_set[rs2]
        )
        self._increment_pc()
        self._increment_clock(cpi)
        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd].base10}")

    def _xor(self, rd: str, rs1: str, rs2: str):
        cpi = CPI_VALUES["xor"]
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)

        self.cpu.register_set[rd] = (
            self.cpu.register_set[rs1] ^ self.cpu.register_set[rs2]
        )
        self._increment_pc()
        self._increment_clock(cpi)
        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd].base10}")

    def _addi(self, rd: str, rs1: str, imm: str):
        cpi = CPI_VALUES["addi"]
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        imm = self._get_imm(imm)

        self.cpu.register_set[rd] = self.cpu.register_set[rs1] + Word(imm)
        self._increment_pc()
        self._increment_clock(cpi)
        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd].base10}")

    def _andi(self, rd: str, rs1: str, imm: str):
        cpi = CPI_VALUES["andi"]
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        imm = self._get_imm(imm)

        self.cpu.register_set[rd] = self.cpu.register_set[rs1] & Word(imm)
        self._increment_pc()
        self._increment_clock(cpi)
        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd].base10}")

    def _ori(self, rd: str, rs1: str, imm: str):
        cpi = CPI_VALUES["ori"]
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        imm = self._get_imm(imm)

        self.cpu.register_set[rd] = self.cpu.register_set[rs1] | Word(imm)
        self._increment_pc()
        self._increment_clock(cpi)
        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd].base10}")

    def _li(self, rd: str, imm: str):
        cpi = CPI_VALUES["li"]
        rd = self._get_register_index(rd)
        imm = self._get_imm(imm)

        self.cpu.register_set[rd] = Word(imm)
        self._increment_pc()
        self._increment_clock(cpi)
        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd].base10}")

    def _beq(self, rs1: str, rs2: str, imm: str):
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)
        imm = self._get_imm(imm)

        if self.cpu.register_set[rs1] == self.cpu.register_set[rs2]:
            self._set_pc(imm)
            cpi = CPI_VALUES["beq_taken"]
        else:
            self._increment_pc()
            cpi = CPI_VALUES["beq_not_taken"]
        self._increment_clock(cpi)

    def _bne(self, rs1: str, rs2: str, imm: str):
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)
        imm = self._get_imm(imm)

        if self.cpu.register_set[rs1] != self.cpu.register_set[rs2]:
            self._set_pc(imm)
            cpi = CPI_VALUES["bne_taken"]
        else:
            self._increment_pc()
            cpi = CPI_VALUES["bne_not_taken"]
        self._increment_clock(cpi)

    def _jal(self, rd: str, imm: str):
        cpi = CPI_VALUES["jal"]
        rd = self._get_register_index(rd)
        self.cpu.register_set[rd] = Word(dez=self._get_pc() + 1)

        imm = self._get_imm(imm)
        self._set_pc(imm)
        self._increment_clock(cpi)
        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd].base10}")

    def _j(self, imm: str):
        cpi = CPI_VALUES["j"]
        imm = self._get_imm(imm)
        self._set_pc(imm)
        self._increment_clock(cpi)

    def _jalr(self, rd: str, rs1_imm: str):
        cpi = CPI_VALUES["jalr"]
        rd = self._get_register_index(rd)
        base, offset = self._get_base_offset(rs1_imm)

        self.cpu.register_set[rd] = Word(dez=self._get_pc() + 4)
        base_value: Word = self.cpu.register_set[base]

        self._set_pc(base_value.dez + offset)
        self._increment_clock(cpi)
        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd].base10}")

    def _lui(self, rd: str, imm: str):
        cpi = CPI_VALUES["lui"]
        rd = self._get_register_index(rd)
        imm = self._get_imm(imm)

        self.cpu.register_set[rd] = Word(dez=imm << 12)
        self._increment_pc()
        self._increment_clock(cpi)
        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd].base10}")

    def _auipc(self, rd: str, imm: str):
        cpi = CPI_VALUES["auipc"]
        rd = self._get_register_index(rd)
        imm = self._get_imm(imm)

        self.cpu.register_set[rd] = Word(dez=self._get_pc() + imm << 12)
        self._increment_pc()
        self._increment_clock(cpi)
        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd].base10}")

    def _lw(self, rd: str, rs1_imm: str):
        cpi = CPI_VALUES["lw"]
        rd = self._get_register_index(rd)
        base, offset = self._get_base_offset(rs1_imm)

        base_val = self.cpu.register_set[base].base10

        self.cpu.register_set[rd] = self.cpu.ram[base_val + offset]
        self._increment_pc()
        logger.info(f"  >> x{rd} = {self.cpu.ram[base_val + offset].base10}")
        self._increment_clock(cpi)

    def _sw(self, rd: str, rs1_imm: str):
        cpi = CPI_VALUES["sw"]
        rd = self._get_register_index(rd)
        base, offset = self._get_base_offset(rs1_imm)

        base_val = self.cpu.register_set[base].base10

        self.cpu.ram[base_val + offset] = self.cpu.register_set[rd]
        self._increment_pc()
        logger.info(
            f"  >> RAM x{self.cpu.ram[base_val + offset].base10} = {self.cpu.register_set[rd].base10}"
        )
        self._increment_clock(cpi)

    def _slt(self, rd: str, rs1: str, rs2: str):
        cpi = CPI_VALUES["slt"]
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)

        if self.cpu.register_set[rs1] < self.cpu.register_set[rs2]:
            self.cpu.register_set[rd] = Word(1)
        else:
            self.cpu.register_set[rd] = Word(0)

        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd]}")
        self._increment_pc()
        self._increment_clock(cpi)

    def _slli(self, rd: str, rs1: str, imm: str):
        cpi = CPI_VALUES["slt"]
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        imm = self._get_imm(imm)

        self.cpu.register_set[rd] = self.cpu.register_set[rs1] << Word(dez=imm)

        logger.info(f"  >> x{rd} = {self.cpu.register_set[rd]}")
        self._increment_pc()
        self._increment_clock(cpi)

    def _ecall(self):
        cpi = CPI_VALUES["ecall"]
        pass
        self._increment_clock(cpi)

    def _ebreak(self):
        cpi = CPI_VALUES["ebreak"]
        pass
        self._increment_clock(cpi)
