6. Summiere Zahlen von 1 bis N
addi x1, x0, 10       # x1 = N = 10
addi x2, x0, 1        # x2 = i = 1
addi x3, x0, 0        # x3 = Summe = 0

loop_sum:
  add  x3, x3, x2     # Summe += i
  addi x2, x2, 1      # i += 1
  bne  x2, x1, loop_sum
add x3, x3, x1        # letzte Addition (i == N)
