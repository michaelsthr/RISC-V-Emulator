# 3. Bedingte Verzweigung (beq)
addi x1, x0, 7        # x1 = 7
addi x2, x0, 7        # x2 = 7
beq  x1, x2, equal    # springe zu 'equal' falls gleich
addi x3, x0, 1        # wird übersprungen

equal:
addi x3, x0, 99       # x3 = 99