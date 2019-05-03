#!/usr/bin/env python3

# The purpose of this program is to provide an interactive substitution cipher decoder.
# The program uses English letter frequency to reccomend the most likely one-to-one
# substitution. It is however up to the user to change the input
# Future hope is to automate the process entirely

import os


SecretMessage = 'GRGZQEGKXJPRQERQEWXJXLDQPHQORRNQRRNGEIZQPTEJRQDVQYZVNQRRNTYZTTKHJPGEZRQEOTJERNTXDQETRTQPRNKQENQWQDVQYZQZZLKTWRNQRNTVQZKJPTGERTDDGITERRNQEWJDXNGEZUTOQLZTNTNQWQONGTFTWZJKLONRNTVNTTDETVYJPSVQPZQEWZJJEVNGDZRQDDRNTWJDXNGEZNQWTFTPWJETVQZKLOSQUJLRGERNTVQRTPNQFGEIQIJJWRGKTULROJEFTPZTDYRNTWJDXNGEZNQWQDVQYZUTDGTFTWRNQRRNTYVTPTHQPKJPTGERTDDGITERRNQEKQEHJPXPTOGZTDYRNTZQKTPTQZJEZOLPGJLZDYTEJLINRNTWJDXNGEZNQWDJEISEJVEJHRNTGKXTEWGEIWTZRPLORGJEJHRNTXDQETRTQPRNQEWNQWKQWTKQEYQRRTKXRZRJQDTPRKQESGEWJHRNTWQEITPULRKJZRJHRNTGPOJKKLEGOQRGJEZVTPTKGZGERTPXPTRTWQZQKLZGEIQRRTKXRZRJXLEONHJJRUQDDZJPVNGZRDTHJPRGWUGRZZJRNTYTFTERLQDDYIQFTLXQEWDTHRRNTTQPRNUYRNTGPJVEKTQEZZNJPRDYUTHJPTRNTFJIJEZQPPGFTWRNTDQZRTFTPWJDXNGEKTZZQITVQZKGZGERTPXPTRTWQZQZLPXPGZGEIDYZJXNGZRGOQRTWQRRTKXRRJWJQWJLUDTUQOSVQPWZZJKTPZQLDRRNPJLINQNJJXVNGDZRVNGZRDGEIRNTZRQPZXQEIDTWUQEETPULRGEHQORRNTKTZZQITVQZRNGZZJDJEIQEWRNQESZHJPQDDRNTHGZNGEHQORRNTPTVQZJEDYJETZXTOGTZJERNTXDQETRKJPTGERTDDGITERRNQEWJDXNGEZQEWRNTYZXTERQDJRJHRNTGPRGKTGEUTNQFGJLPQDPTZTQPONDQUJPQRJPGTZPLEEGEIPJLEWGEZGWTVNTTDZQEWOJEWLORGEIHPGINRTEGEIDYTDTIQERQEWZLURDTTBXTPGKTERZJEKQERNTHQORRNQRJEOTQIQGEKQEOJKXDTRTDYKGZGERTPXPTRTWRNGZPTDQRGJEZNGXVQZTERGPTDYQOOJPWGEIRJRNTZTOPTQRLPTZXDQEZ'
SecretMessage = list(SecretMessage)

letterdict = {}

for i in range (26):
    letter = chr(i+65)
    letterdict[letter] = 0

for i in SecretMessage:
    letterdict[str(i)] += 1
        # Creates letter dictionary, counts the instances of those letters
        # in the ciphertext, forming a letter-instance dictionary


FreqList = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
FreqList = list(FreqList)

ThisFreqList = []
for w in sorted(letterdict, key=letterdict.get, reverse=True):
    ThisFreqList.append(w)


dictionary = dict(zip(ThisFreqList,FreqList))
        # ThisFreqList-a sorted list of letter frequencies in the given sample
        # FreqList, taken from the internet, as the most common English letters
        # A new dictionary is created to relate these two 



SecretMessage = ''.join(SecretMessage)
blank = '-'*len(SecretMessage)
        # The secret message is converted into a string again and a 
        # 'tick string' is created of equal length



# Change() is the function that will ask for user input of what letters to 
# substitute for which. All instances of the letter are changed and the 
# corresponding 'tick' mark is changed as well

def Change():
    global SecretMessage
    global blank
    change = input("enter what to change: eg 'em' changes E to M (case insensitive): ")
    change = change.upper()
    print(change)
    initial = change[0]
    final = change[1]
    while initial in SecretMessage:
        global index
        index = SecretMessage.find(initial)
        blank = list(blank)
        blank[index] = final
        blank = ''.join(blank)
        SecretMessage = SecretMessage.replace(SecretMessage[index],SecretMessage[index].lower(),1)
    SecretMessage = SecretMessage.replace(SecretMessage[index].lower(),SecretMessage[index].upper())

# The main functionality, while blank ticks still exist, this will display the
# recomended changes and call the Change() function
os.system("printf '\e[8;40;168t'")
    # resize terminal for user experience
while '-' in blank:
    os.system('clear')
    print('recommended changes based on frequency analysis:')
    print("\n\nchange from:",' '.join(ThisFreqList))
    print("change to  :",' '.join(FreqList),"\t\tuse your judgement, 't-e' may be 'the', etc... Good Luck!",'\n\n')



    longlistSecretMessage = []
    longlistblank = []
    measure = len(SecretMessage)//8
    for i in range(len(SecretMessage)//measure+1):
        longlistSecretMessage.append(SecretMessage[0+i*measure:measure+i*measure])
        longlistblank.append(blank[0+i*measure:measure+i*measure])

    for i in range(len(longlistSecretMessage)):
        print(longlistblank[i])
        print(longlistSecretMessage[i])
        print()
    # The above splits the message into reasonablly-sized chunks, placing
    # those in a list so they can be displayed on top of eachother for ease
    # of comparison when choosing which letters to replace
    Change()



print('done? I suppose yourfinal message is:')
print(blank)


"""    The following automatically replaces each entry without prompting the 
        user, it's very flawed right now unfortunately
Message = []
for i in SecretMessage:
    Message.append(dictionary[i])

Message = ''.join(Message)

print(Message)
"""
