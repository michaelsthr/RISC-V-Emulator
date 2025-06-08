4. Unbedingter Sprung (jal)
jal  x0, target       # Sprung ohne Rückkehr
addi x1, x0, 1        # wird übersprungen

target:
addi x2, x0, 2        # x2 = 2
