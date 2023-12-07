#!/usr/bin/env python3

#Outputs all 26 possibilities of a Caesar shift cipher

import numpy as np

SecretMessage = 'tnspnvpotegpcjeszczfrswjdltoespnzxafepclyoeslebftepopqtytepwjtdesplydhpctestyvespaczmwpxezmpbftepszypdehtesjzftdeslejzfgpypgpclneflwwjvyzhyhsleespbfpdetzytd'

SecretMessage='KHAQWVTACPFVCMGCECVCRCTVVQUGGJQYKVYQTMUVJGHKTUVVJKPIAQWJCXGQPAQWTJCPFUKUCPQPYQTMKPIECV'

SecretMessage = list(SecretMessage)

EncodedList = []

for i in SecretMessage:
    EncodedList.append(ord(i.lower())-97)

            # ascii characters for lower case are a-z, 97-122, so subtracting
            # 97 gives us characters from 0-25, this can then be shifted upward
            # and modded by 26 to keep everything a-z

EncodedArray = np.asarray(EncodedList)

for i in range(26):
    Message = []
    for j in EncodedArray:
        j = (j+i)%26
        Message.append(chr(j+97))
    print("Shifted up by",i,' (i.e. a ->',chr(97+i),'):')
    print(''.join(Message),'\n')


