from typing import TYPE_CHECKING
from loguru import logger

from .register_set import RegisterSet
from .word import Word

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

    # --- INSTRUCTIONS ---

    def _add(self, rd: str, rs1: str, rs2: str):
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)

        self.cpu.register_set[rd] = (
            self.cpu.register_set[rs1] + self.cpu.register_set[rs2]
        )
        self._increment_pc()

    def _sub(self, rd: str, rs1: str, rs2: str):
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)

        self.cpu.register_set[rd] = (
            self.cpu.register_set[rs1] - self.cpu.register_set[rs2]
        )
        self._increment_pc()

    def _and(self, rd: str, rs1: str, rs2: str):
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)

        self.cpu.register_set[rd] = (
            self.cpu.register_set[rs1] & self.cpu.register_set[rs2]
        )
        self._increment_pc()

    def _or(self, rd: str, rs1: str, rs2: str):
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)

        self.cpu.register_set[rd] = (
            self.cpu.register_set[rs1] | self.cpu.register_set[rs2]
        )
        self._increment_pc()

    def _xor(self, rd: str, rs1: str, rs2: str):
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)

        self.cpu.register_set[rd] = (
            self.cpu.register_set[rs1] ^ self.cpu.register_set[rs2]
        )
        self._increment_pc()

    def _addi(self, rd: str, rs1: str, imm: str):
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        imm = self._get_imm(imm)

        self.cpu.register_set[rd] = self.cpu.register_set[rs1] + Word(imm)
        self._increment_pc()

    def _andi(self, rd: str, rs1: str, imm: str):
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        imm = self._get_imm(imm)

        self.cpu.register_set[rd] = self.cpu.register_set[rs1] & Word(imm)
        self._increment_pc()

    def _ori(self, rd: str, rs1: str, imm: str):
        rd = self._get_register_index(rd)
        rs1 = self._get_register_index(rs1)
        imm = self._get_imm(imm)

        self.cpu.register_set[rd] = self.cpu.register_set[rs1] | Word(imm)
        self._increment_pc()

    def _li(self, rd: str, imm: str):
        rd = self._get_register_index(rd)
        imm = self._get_imm(imm)

        self.cpu.register_set[rd] = Word(imm)
        self._increment_pc()

    def _beq(self, rs1: str, rs2: str, imm: str):
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)
        imm = self._get_imm(imm)

        if self.cpu.register_set[rs1] == self.cpu.register_set[rs2]:
            self.pc = imm
        else:
            self._increment_pc()

    def _bne(self, rs1: str, rs2: str, imm: str):
        rs1 = self._get_register_index(rs1)
        rs2 = self._get_register_index(rs2)
        imm = self._get_imm(imm)

        if self.cpu.register_set[rs1] != self.cpu.register_set[rs2]:
            self.pc = imm
        else:
            self._increment_pc()

    def _jal(self, rd: str, imm: str):
        rd = self._get_register_index(rd)
        self.cpu.register_set[rd] = Word(dez=self._get_pc())

        imm = self._get_imm(imm)
        self._set_pc(imm)

    def _j(self, imm: str):
        imm = self._get_imm(imm)
        self._set_pc(imm)

    def _jalr(self, rd: str, rs1_imm: str):
        rd = self._get_register_index(rd)
        base, offset = self._get_base_offset(rs1_imm)

        self.cpu.register_set[rd] = Word(dez=self._get_pc() + 4)
        base_value: Word = self.cpu.register_set[base]

        self._set_pc(base_value.dez + offset)

    def _lui(self, rd: str, imm: str):
        rd_idx = self._get_register_index(rd)
        imm = self._get_imm(imm)

        self.cpu.register_set[rd_idx] = Word(dez=imm << 12)
        self._increment_pc()

    def _auipc(self, rd: str, imm: str):
        rd_idx = self._get_register_index(rd)
        imm = self._get_imm(imm)

        self.cpu.register_set[rd_idx] = Word(dez=self._get_pc() + imm << 12)
        self._increment_pc()
