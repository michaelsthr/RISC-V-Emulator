# 5. Schleife (zähle rückwärts)
addi x1, x0, 5        # x1 = 5 (Zähler)

loop:
  addi x1, x1, -1     # x1 -= 1
  bne  x1, x0, loop   # solange x1 != 0, wiederhole
