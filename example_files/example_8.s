# 8. Maximum in einem Array finden
#
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# Array liegt ab Adresse 100
# Laenge = 5 Elemente (4 Byte pro Element )
# Ergebnis(Maximum) in x3
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−

addi x1, x0, 100      # x1 = Basisadresse des Arrays
addi x2, x0, 5        # x2 = Anzahl Elemente
addi x4, x1, 0        # x4 = Zeiger ins Array
lw   x3, 0(x4)        # x3 = erstes Element (Initial-Maximum)
addi x2, x2, -1       # x2 = verbleibende Elemente

loop_max:
  addi x4, x4, 4      # Zeiger += 4 (nächstes Element)
  lw   x5, 0(x4)      # x5 = aktuelles Element
  slt  x6, x3, x5     # x6 = 1, wenn x3 < x5
  bne  x6, x0, update # falls größer: update

cont:
  addi x2, x2, -1     # nächstes Element
  bne  x2, x0, loop_max
  j end

update:
  add  x3, x5, x0     # x3 = neues Maximum
  j cont

end:
# x3 = Maximum
