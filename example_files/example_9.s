9. Funktionsaufruf mit jal / jalr
addi x1, x0, 21       # x1 = 21
jal  x5, double       # Aufruf, Rücksprungadresse in x5
j    end              # nach Rückkehr

double:
  slli x6, x1, 1      # x6 = x1 << 1 = x1 * 2
  jalr x0, 0(x5)      # Rücksprung über x5

end:
# x6 = 42