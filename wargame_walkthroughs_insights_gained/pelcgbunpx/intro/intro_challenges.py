from pwn import xor
#uggcf://pelcgbunpx.bet/pbhefrf/vageb/kbexrl1/

# UVAG: Lbh rvgure xabj, KBE lbh qba'g. V'ir rapelcgrq gur synt jvgu zl frperg xrl, lbh'yy arire or noyr gb thrff vg. Erzrzore gur synt sbezng naq ubj vg zvtug uryc lbh va guvf punyyratr!

ciphertext="0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"

partial = xor(bytes.fromhex(ciphertext),b"crypto{")
print(partial.decode())

#OUTPUT: myXORke+y_Q\x0bHOMe$~seG8bGURN\x04DFWg)a|\x1dTM!an\x7f

#znxrf vg boivbhf vg'f zlKBExrl, fb jr pna qrpbqr gur shyy guvat
print( xor(bytes.fromhex(ciphertext),b'myXORkey') )

