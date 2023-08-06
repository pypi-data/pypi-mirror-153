####################################################################
#/ Nom du projet: py-zpp_serpent                                  /#
#/ Nom du fichier: serpent.py                                     /#
#/ Type de fichier: fichier principal                             /#
#/ Fichier annexe:                                                /#
#/                                                                /#
#/ Auteur: ZephyrOff  (Alexandre Pajak)                           /#
#/ Version: 2.2.1                                                 /#
#/ Description: Implémentation du chiffrement Serpent             /#
#/ Date: 01/06/2022                                               /#
####################################################################

import re
import os
import hashlib
from bitstring import BitArray


def SHat(box, input):
    result = ""
    for i in range(32):
        result = result + SBoxBitstring[box%8][input[4*i:4*(i+1)]]
    return result

def SHatInverse(box, output):
    result = ""
    for i in range(32):
        result = result + SBoxBitstringInverse[box%8][output[4*i:4*(i+1)]]
    return result     

def LT(input):
    if len(input) != 128:
        raise ValueError("input to LT is not 128 bit long")

    result = ""
    for i in range(len(LTTable)):
        outputBit = "0"
        for j in LTTable[i]:
            outputBit = xor(outputBit, input[j])
        result = result + outputBit
    return result

def LTInverse(output):
    if len(output) != 128:
        raise ValueError("input to inverse LT is not 128 bit long")

    result = ""
    for i in range(len(LTTableInverse)):
        inputBit = "0"
        for j in LTTableInverse[i]:
            inputBit = xor(inputBit, output[j])
        result = result + inputBit
    return result

def applyPermutation(permutationTable, input):
    if len(input) != len(permutationTable):
        raise ValueError("input size (%d) doesn't match perm table size (%d)"% (len(input), len(permutationTable)))
    result = ""
    for i in range(len(permutationTable)):
        result = result + input[permutationTable[i]]
    return result

def R(i, BHati, KHat):
    xored = xor(BHati, KHat[i])
    SHati = SHat(i, xored)

    if 0 <= i <= r-2:
        BHatiPlus1 = LT(SHati)
    elif i == r-1:
        BHatiPlus1 = xor(SHati, KHat[r])
    else:
        raise ValueError("round %d is out of 0..%d range" % (i, r-1))

    return BHatiPlus1

def RInverse(i, BHatiPlus1, KHat):
    if 0 <= i <= r-2:
        SHati = LTInverse(BHatiPlus1)
    elif i == r-1:
        SHati = xor(BHatiPlus1, KHat[r])
    else:
        raise ValueError("round %d is out of 0..%d range" % (i, r-1))
    xored = SHatInverse(i, SHati)
    BHati = xor(xored, KHat[i])

    return BHati

def encrypt(plainText, userKey):
    K, KHat = makeSubkeys(userKey)
    BHat = applyPermutation(IPTable, plainText)
    for i in range(r):
        BHat = R(i, BHat, KHat)
    C = applyPermutation(FPTable, BHat)

    return C

def decrypt(cipherText, userKey):
    K, KHat = makeSubkeys(userKey)
    BHat = applyPermutation(IPTable, cipherText)
    for i in range(r-1, -1, -1):
        BHat = RInverse(i, BHat, KHat)
    plainText = applyPermutation(FPTable, BHat)

    return plainText

def encrypt_ECB(plainText,userKey,hash_type='sha256',lvl=2):
    salt = os.urandom(SALT_SIZE)
    key = hashlib.pbkdf2_hmac(hash_type, userKey, salt, 100000,dklen=KEY_SIZE)

    key = BitArray(key).bin
    cleartext = BitArray(plainText).bin
    result=BitArray(bin=encrypt(BitArray(salt).bin,BitArray(hashlib.sha256(userKey).digest()).bin)).bytes

    if len(cleartext)<=128:
        lvl=1
        bloclist = []
        bloclist.append(cleartext)
    else:
        bloclist = re.findall('.{1,128}', cleartext)

        if lvl==1:
            liste = bloclist[0:len(bloclist)-1]
        elif lvl==2:
            liste = bloclist[0:len(bloclist)-2]


        for bloc in liste:
            encrypted = encrypt(bloc, key)
            result += BitArray(bin=encrypted).bytes

    if lvl==1:
        bloc = bloclist[len(bloclist)-1]
        if len(bloc)!=128:
            bloc = add_rembour(bloc)
        encrypted = encrypt(bloc, key)
        result += BitArray(bin=encrypted).bytes

    elif lvl==2:
        blocA = encrypt(bloclist[len(bloclist)-2],key)
        blocB = bloclist[len(bloclist)-1]
        sbreak = 128-len(blocB)
        blocA2 = blocA[0:len(blocA)-sbreak]
        blocAdd = blocA[len(blocA)-sbreak:len(blocA)]

        blocB2 = encrypt(blocB+blocAdd,key)

        result += BitArray(bin=blocB2).bytes
        result += BitArray(bin=blocA2).bytes

    return result

def encrypt_CBC(plainText,userKey,hash_type='sha256',lvl=2):
    salt = os.urandom(SALT_SIZE)
    derived = hashlib.pbkdf2_hmac(hash_type, userKey, salt, 100000,dklen=IV_SIZE + KEY_SIZE)

    key = BitArray(derived[IV_SIZE:]).bin
    cleartext = BitArray(plainText).bin
    iv = BitArray(derived[0:IV_SIZE]).bin
    result=BitArray(bin=encrypt(BitArray(salt).bin,BitArray(hashlib.sha256(userKey).digest()).bin)).bytes
    
    if len(cleartext)<=128:
        lvl=1
        bloclist = []
        bloclist.append(cleartext)
    else:
        bloclist = re.findall('.{1,128}', cleartext)

        if lvl==1:
            liste = bloclist[0:len(bloclist)-1]
        elif lvl==2:
            liste = bloclist[0:len(bloclist)-2]

        for bloc in liste:
            bloc = binaryXor(bloc,iv)
            encrypted = encrypt(bloc, key)

            iv = encrypted
            result += BitArray(bin=encrypted).bytes

    if lvl==1:
        bloc = bloclist[len(bloclist)-1]
        if len(bloc)!=128:
            bloc = add_rembour(bloc)

        bloc = binaryXor(bloc,iv)
        encrypted = encrypt(bloc, key)
        result += BitArray(bin=encrypted).bytes

    elif lvl==2:
        blocA = binaryXor(bloclist[len(bloclist)-2], iv)
        blocA = encrypt(blocA,key)

        blocB = bloclist[len(bloclist)-1]
        sbreak = 128-len(blocB)

        blocA2 = blocA[0:len(blocA)-sbreak]

        blocB += "0"*sbreak
        blocB = binaryXor(blocA, blocB)
        blocB2 = encrypt(blocB,key)

        result += BitArray(bin=blocB2).bytes
        result += BitArray(bin=blocA2).bytes

    return result

def encrypt_CFB(plainText,userKey,hash_type='sha256'):
    salt = os.urandom(SALT_SIZE)
    derived = hashlib.pbkdf2_hmac(hash_type, userKey, salt, 100000,dklen=IV_SIZE + KEY_SIZE)

    key = BitArray(derived[IV_SIZE:]).bin
    cleartext = BitArray(plainText).bin
    iv = BitArray(derived[0:IV_SIZE]).bin
    liste = re.findall('.{1,128}', cleartext)

    result=BitArray(bin=encrypt(BitArray(salt).bin,BitArray(hashlib.sha256(userKey).digest()).bin)).bytes
    for bloc in liste:
        if len(bloc)!=128:
            bloc = add_rembour(bloc)

        encrypted = encrypt(iv, key)
        bloc = binaryXor(bloc,encrypted)
        iv = bloc
        result += BitArray(bin=bloc).bytes
    return result

def encrypt_PCBC(plainText,userKey,hash_type='sha256'):
    salt = os.urandom(SALT_SIZE)
    derived = hashlib.pbkdf2_hmac(hash_type, userKey, salt, 100000,dklen=IV_SIZE + KEY_SIZE)

    key = BitArray(derived[IV_SIZE:]).bin
    cleartext = BitArray(plainText).bin
    iv = BitArray(derived[0:IV_SIZE]).bin
    liste = re.findall('.{1,128}', cleartext)

    result=BitArray(bin=encrypt(BitArray(salt).bin,BitArray(hashlib.sha256(userKey).digest()).bin)).bytes

    for bloc in liste:
        if len(bloc)!=128:
            bloc = add_rembour(bloc)

        blocxor = binaryXor(bloc,iv)
        encrypted = encrypt(blocxor, key)
        iv = binaryXor(bloc,encrypted)
        result += BitArray(bin=encrypted).bytes
    return result

def decrypt_ECB(cipherText,userKey,hash_type='sha256',lvl=2):
    salt = BitArray(bin=decrypt(BitArray(cipherText[0:SALT_SIZE]).bin,BitArray(hashlib.sha256(userKey).digest()).bin)).bytes
    key = hashlib.pbkdf2_hmac(hash_type, userKey, salt, 100000,dklen=KEY_SIZE)

    key = BitArray(key).bin
    cipherText = BitArray(cipherText[SALT_SIZE:]).bin
    result=b""

    if len(cipherText)<=128:
        lvl=1
        bloclist = []
        bloclist.append(cipherText)
    else:
        bloclist = re.findall('.{1,128}', cipherText)

        if lvl==1:
            liste = bloclist[0:len(bloclist)-1]
        elif lvl==2:
            liste = bloclist[0:len(bloclist)-2]

        for bloc in liste:
            encrypted = decrypt(bloc, key)
            result += BitArray(bin=encrypted).bytes

    if lvl==1:
        last_bloc = decrypt(bloclist[len(bloclist)-1], key)
        result+=del_rembour(last_bloc)
    elif lvl==2:
        blocA = decrypt(bloclist[len(bloclist)-2],key)
        blocB = bloclist[len(bloclist)-1]
        sbreak = 128-len(blocB)

        blocA2 = blocA[0:len(blocA)-sbreak]
        blocAdd = blocA[len(blocA)-sbreak:len(blocA)]

        blocB2 = decrypt(blocB+blocAdd,key)

        result += BitArray(bin=blocB2).bytes
        result += BitArray(bin=blocA2).bytes

    return result

def decrypt_CBC(cipherText,userKey,hash_type='sha256',lvl=2):
    salt = BitArray(bin=decrypt(BitArray(cipherText[0:SALT_SIZE]).bin,BitArray(hashlib.sha256(userKey).digest()).bin)).bytes
    derived = hashlib.pbkdf2_hmac(hash_type, userKey, salt, 100000,dklen=IV_SIZE + KEY_SIZE)

    key = BitArray(derived[IV_SIZE:]).bin
    cipherText = BitArray(cipherText[SALT_SIZE:]).bin
    iv = BitArray(derived[0:IV_SIZE]).bin
    result=b""

    if len(cipherText)<=128:
        lvl=1
        bloclist = []
        bloclist.append(cipherText)
    else:
        bloclist = re.findall('.{1,128}', cipherText)

        if lvl==1:
            liste = bloclist[0:len(bloclist)-1]
        elif lvl==2:
            liste = bloclist[0:len(bloclist)-2]

        for bloc in liste:
            encrypted = decrypt(bloc, key)
            encrypted = binaryXor(encrypted,iv)
            result += BitArray(bin=encrypted).bytes
            iv = bloc

    if lvl==1:
        last_bloc = decrypt(bloclist[len(bloclist)-1], key)
        last_bloc = binaryXor(last_bloc,iv)
        result+=del_rembour(last_bloc)
    elif lvl==2:
        blocA = bloclist[len(bloclist)-2]
        blocB = bloclist[len(bloclist)-1]
        sbreak = 128-len(blocB)

        blocA = decrypt(blocA, key)

        blocB+=blocA[len(blocA)-sbreak:len(blocA)]
        blocA = binaryXor(blocA,blocB)

        blocB = decrypt(blocB,key)
        blocB = binaryXor(blocB,iv)

        result += BitArray(bin=blocB).bytes
        result += BitArray(bin=blocA).bytes

    return result

def decrypt_CFB(cipherText,userKey,hash_type='sha256'):
    salt = BitArray(bin=decrypt(BitArray(cipherText[0:SALT_SIZE]).bin,BitArray(hashlib.sha256(userKey).digest()).bin)).bytes
    derived = hashlib.pbkdf2_hmac(hash_type, userKey, salt, 100000,dklen=IV_SIZE + KEY_SIZE)

    key = BitArray(derived[IV_SIZE:]).bin
    cipherText = BitArray(cipherText[SALT_SIZE:]).bin
    iv = BitArray(derived[0:IV_SIZE]).bin
    liste = re.findall('.{1,128}', cipherText)

    result=b""
    for bloc in liste[0:len(liste)-1]:
        encrypted = encrypt(iv, key)
        encrypted = binaryXor(encrypted,bloc)
        result += BitArray(bin=encrypted).bytes
        iv = bloc

    encrypted = encrypt(iv, key)
    last_bloc = binaryXor(encrypted,liste[len(liste)-1])
    result+=del_rembour(last_bloc)

    return result

def decrypt_PCBC(cipherText,userKey,hash_type='sha256'):
    salt = BitArray(bin=decrypt(BitArray(cipherText[0:SALT_SIZE]).bin,BitArray(hashlib.sha256(userKey).digest()).bin)).bytes
    derived = hashlib.pbkdf2_hmac(hash_type, userKey, salt, 100000,dklen=IV_SIZE + KEY_SIZE)

    key = BitArray(derived[IV_SIZE:]).bin
    cipherText = BitArray(cipherText[SALT_SIZE:]).bin
    iv = BitArray(derived[0:IV_SIZE]).bin
    liste = re.findall('.{1,128}', cipherText)

    result=b""
    for bloc in liste[0:len(liste)-1]:
        encrypted = decrypt(bloc, key)
        encrypted = binaryXor(encrypted,iv)
        iv = binaryXor(encrypted,bloc)
        result += BitArray(bin=encrypted).bytes

    encrypted = decrypt(liste[len(liste)-1], key)
    last_bloc = binaryXor(encrypted,iv)
    result+=del_rembour(last_bloc)

    return result

def add_rembour(bloc):
    rep = round((128-len(bloc))/8)
    if rep<10:
        bour="0"+str(rep)
    else:
        bour=str(rep)
    pattern = (BitArray(hex=bour).bin)*rep
    bloc += pattern

    return bloc

def del_rembour(bloc):
    for i in range(32,0,-1):
        if i<10:
            bour="0"+str(i)
        else:
            bour=str(i)
        pattern = (BitArray(hex=bour).bin)*i
        if bloc.endswith(pattern):
            return BitArray(bin=bloc[:-(i*8)]).bytes
            
    return BitArray(bin=bloc).bytes

def makeSubkeys(userKey):
    w = {}
    for i in range(-8, 0):
        w[i] = userKey[(i+8)*32:(i+9)*32]

    for i in range(132):
        w[i] = rotateLeft(xor(w[i-8], w[i-5], w[i-3], w[i-1],bitstring(phi, 32), bitstring(i,32)),11)

    k = {}
    for i in range(r+1):
        whichS = (r + 3 - i) % r
        k[0+4*i] = ""
        k[1+4*i] = ""
        k[2+4*i] = ""
        k[3+4*i] = ""
        for j in range(32):
            input = w[0+4*i][j] + w[1+4*i][j] + w[2+4*i][j] + w[3+4*i][j]
            output = SBoxBitstring[whichS%8][input]
            for l in range(4):
                k[l+4*i] = k[l+4*i] + output[l]
    K = []
    for i in range(33):
        K.append(k[4*i] + k[4*i+1] + k[4*i+2] + k[4*i+3])

    KHat = []
    for i in range(33):
        KHat.append(applyPermutation(IPTable, K[i]))

    return K, KHat

def bitstring(n, minlen=1):
    if minlen < 1:
        raise ValueError("a bitstring must have at least 1 char")
    if n < 0:
        raise ValueError("bitstring representation undefined for neg numbers")

    result = ""
    while n > 0:
        if n & 1:
            result = result + "1"
        else:
            result = result + "0"
        n = n >> 1
    if len(result) < minlen:
        result = result + "0" * (minlen - len(result))
    return result

def binaryXor(n1, n2):
    if len(n1) != len(n2):
        raise ValueError("can't xor bitstrings of different " + "lengths (%d and %d)" % (len(n1), len(n2)))
    result = ""
    for i in range(len(n1)):
        if n1[i] == n2[i]:
            result = result + "0"
        else:
            result = result + "1"
    return result

def xor(*args):
    if args == []:
        raise ValueError("at least one argument needed")
    result = args[0]
    for arg in args[1:]:
        result = binaryXor(result, arg)
    return result

def rotateLeft(input, places):
    p = places % len(input)
    return input[-p:] + input[:-p]
            
# Constants
IV_SIZE = 16
KEY_SIZE = 32
SALT_SIZE = 16
phi = 2654435769
r = 32

# Data tables
SBoxDecimalTable = [[ 3, 8,15, 1,10, 6, 5,11,14,13, 4, 2, 7, 0, 9,12 ],[15,12, 2, 7, 9, 0, 5,10, 1,11,14, 8, 6,13, 3, 4 ],[ 8, 6, 7, 9, 3,12,10,15,13, 1,14, 4, 0,11, 5, 2 ],[ 0,15,11, 8,12, 9, 6, 3,13, 1, 2, 4,10, 7, 5,14 ],[ 1,15, 8, 3,12, 0,11, 6, 2, 5, 4,10, 9,14, 7,13 ],[15, 5, 2,11, 4,10, 9,12, 0, 3,14, 8,13, 6, 7, 1 ],[ 7, 2,12, 5, 8, 4, 6,11,14, 9, 1,15,13, 3,10, 0 ],[ 1,13,15, 0,14, 8, 2,11, 7, 4,12,10, 9, 3, 5, 6 ]] 

SBoxBitstring = []
SBoxBitstringInverse = []
for line in SBoxDecimalTable:
    dict = {}
    inverseDict = {}
    for i in range(len(line)):
        index = bitstring(i, 4)
        value = bitstring(line[i], 4)
        dict[index] = value
        inverseDict[value] = index
    SBoxBitstring.append(dict)
    SBoxBitstringInverse.append(inverseDict)


IPTable = [0, 32, 64, 96, 1, 33, 65, 97, 2, 34, 66, 98, 3, 35, 67, 99,4, 36, 68, 100, 5, 37, 69, 101, 6, 38, 70, 102, 7, 39, 71, 103,8, 40, 72, 104, 9, 41, 73, 105, 10, 42, 74, 106, 11, 43, 75, 107,12, 44, 76, 108, 13, 45, 77, 109, 14, 46, 78, 110, 15, 47, 79, 111,16, 48, 80, 112, 17, 49, 81, 113, 18, 50, 82, 114, 19, 51, 83, 115,20, 52, 84, 116, 21, 53, 85, 117, 22, 54, 86, 118, 23, 55, 87, 119,24, 56, 88, 120, 25, 57, 89, 121, 26, 58, 90, 122, 27, 59, 91, 123,28, 60, 92, 124, 29, 61, 93, 125, 30, 62, 94, 126, 31, 63, 95, 127]
FPTable = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60,64, 68, 72, 76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120, 124,1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61,65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121, 125,2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62,66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 118, 122, 126,3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63,67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 107, 111, 115, 119, 123, 127]
LTTable = [[16, 52, 56, 70, 83, 94, 105],[72, 114, 125],[2, 9, 15, 30, 76, 84, 126],[36, 90, 103],[20, 56, 60, 74, 87, 98, 109],[1, 76, 118],[2, 6, 13, 19, 34, 80, 88],[40, 94, 107],[24, 60, 64, 78, 91, 102, 113],[5, 80, 122],[6, 10, 17, 23, 38, 84, 92],[44, 98, 111],[28, 64, 68, 82, 95, 106, 117],[9, 84, 126],[10, 14, 21, 27, 42, 88, 96],[48, 102, 115],[32, 68, 72, 86, 99, 110, 121],[2, 13, 88],[14, 18, 25, 31, 46, 92, 100],[52, 106, 119],[36, 72, 76, 90, 103, 114, 125],[6, 17, 92],[18, 22, 29, 35, 50, 96, 104],[56, 110, 123],[1, 40, 76, 80, 94, 107, 118],[10, 21, 96],[22, 26, 33, 39, 54, 100, 108],[60, 114, 127],[5, 44, 80, 84, 98, 111, 122],[14, 25, 100],[26, 30, 37, 43, 58, 104, 112],[3, 118],[9, 48, 84, 88, 102, 115, 126],[18, 29, 104],[30, 34, 41, 47, 62, 108, 116],[7, 122],[2, 13, 52, 88, 92, 106, 119],[22, 33, 108],[34, 38, 45, 51, 66, 112, 120],[11, 126],[6, 17, 56, 92, 96, 110, 123],[26, 37, 112],[38, 42, 49, 55, 70, 116, 124],[2, 15, 76],[10, 21, 60, 96, 100, 114, 127],[30, 41, 116],[0, 42, 46, 53, 59, 74, 120],[6, 19, 80],[3, 14, 25, 100, 104, 118],[34, 45, 120],[4, 46, 50, 57, 63, 78, 124],[10, 23, 84],[7, 18, 29, 104, 108, 122],[38, 49, 124],[0, 8, 50, 54, 61, 67, 82],[14, 27, 88],[11, 22, 33, 108, 112, 126],[0, 42, 53],[4, 12, 54, 58, 65, 71, 86],[18, 31, 92],[2, 15, 26, 37, 76, 112, 116],[4, 46, 57],[8, 16, 58, 62, 69, 75, 90],[22, 35, 96],[6, 19, 30, 41, 80, 116, 120],[8, 50, 61],[12, 20, 62, 66, 73, 79, 94],[26, 39, 100],[10, 23, 34, 45, 84, 120, 124],[12, 54, 65],[16, 24, 66, 70, 77, 83, 98],[30, 43, 104],[0, 14, 27, 38, 49, 88, 124],[16, 58, 69],[20, 28, 70, 74, 81, 87, 102],[34, 47, 108],[0, 4, 18, 31, 42, 53, 92],[20, 62, 73],[24, 32, 74, 78, 85, 91, 106],[38, 51, 112],[4, 8, 22, 35, 46, 57, 96],[24, 66, 77],[28, 36, 78, 82, 89, 95, 110],[42, 55, 116],[8, 12, 26, 39, 50, 61, 100],[28, 70, 81],[32, 40, 82, 86, 93, 99, 114],[46, 59, 120],[12, 16, 30, 43, 54, 65, 104],[32, 74, 85],[36, 90, 103, 118],[50, 63, 124],[16, 20, 34, 47, 58, 69, 108],[36, 78, 89],[40, 94, 107, 122],[0, 54, 67],[20, 24, 38, 51, 62, 73, 112],[40, 82, 93],[44, 98, 111, 126],[4, 58, 71],[24, 28, 42, 55, 66, 77, 116],[44, 86, 97],[2, 48, 102, 115],[8, 62, 75],[28, 32, 46, 59, 70, 81, 120],[48, 90, 101],[6, 52, 106, 119],[12, 66, 79],[32, 36, 50, 63, 74, 85, 124],[52, 94, 105],[10, 56, 110, 123],[16, 70, 83],[0, 36, 40, 54, 67, 78, 89],[56, 98, 109],[14, 60, 114, 127],[20, 74, 87],[4, 40, 44, 58, 71, 82, 93],[60, 102, 113],[3, 18, 72, 114, 118, 125],[24, 78, 91],[8, 44, 48, 62, 75, 86, 97],[64, 106, 117],[1, 7, 22, 76, 118, 122],[28, 82, 95],[12, 48, 52, 66, 79, 90, 101],[68, 110, 121],[5, 11, 26, 80, 122, 126],[32, 86, 99],]
LTTableInverse = [[53, 55, 72],[1, 5, 20, 90],[15, 102],[3, 31, 90],[57, 59, 76],[5, 9, 24, 94],[19, 106],[7, 35, 94],[61, 63, 80],[9, 13, 28, 98],[23, 110],[11, 39, 98],[65, 67, 84],[13, 17, 32, 102],[27, 114],[1, 3, 15, 20, 43, 102],[69, 71, 88],[17, 21, 36, 106],[1, 31, 118],[5, 7, 19, 24, 47, 106],[73, 75, 92],[21, 25, 40, 110],[5, 35, 122],[9, 11, 23, 28, 51, 110],[77, 79, 96],[25, 29, 44, 114],[9, 39, 126],[13, 15, 27, 32, 55, 114],[81, 83, 100],[1, 29, 33, 48, 118],[2, 13, 43],[1, 17, 19, 31, 36, 59, 118],[85, 87, 104],[5, 33, 37, 52, 122],[6, 17, 47],[5, 21, 23, 35, 40, 63, 122],[89, 91, 108],[9, 37, 41, 56, 126],[10, 21, 51],[9, 25, 27, 39, 44, 67, 126],[93, 95, 112],[2, 13, 41, 45, 60],[14, 25, 55],[2, 13, 29, 31, 43, 48, 71],[97, 99, 116],[6, 17, 45, 49, 64],[18, 29, 59],[6, 17, 33, 35, 47, 52, 75],[101, 103, 120],[10, 21, 49, 53, 68],[22, 33, 63],[10, 21, 37, 39, 51, 56, 79],[105, 107, 124],[14, 25, 53, 57, 72],[26, 37, 67],[14, 25, 41, 43, 55, 60, 83],[0, 109, 111],[18, 29, 57, 61, 76],[30, 41, 71],[18, 29, 45, 47, 59, 64, 87],[4, 113, 115],[22, 33, 61, 65, 80],[34, 45, 75],[22, 33, 49, 51, 63, 68, 91],[8, 117, 119],[26, 37, 65, 69, 84],[38, 49, 79],[26, 37, 53, 55, 67, 72, 95],[12, 121, 123],[30, 41, 69, 73, 88],[42, 53, 83],[30, 41, 57, 59, 71, 76, 99],[16, 125, 127],[34, 45, 73, 77, 92],[46, 57, 87],[34, 45, 61, 63, 75, 80, 103],[1, 3, 20],[38, 49, 77, 81, 96],[50, 61, 91],[38, 49, 65, 67, 79, 84, 107],[5, 7, 24],[42, 53, 81, 85, 100],[54, 65, 95],[42, 53, 69, 71, 83, 88, 111],[9, 11, 28],[46, 57, 85, 89, 104],[58, 69, 99],[46, 57, 73, 75, 87, 92, 115],[13, 15, 32],[50, 61, 89, 93, 108],[62, 73, 103],[50, 61, 77, 79, 91, 96, 119],[17, 19, 36],[54, 65, 93, 97, 112],[66, 77, 107],[54, 65, 81, 83, 95, 100, 123],[21, 23, 40],[58, 69, 97, 101, 116],[70, 81, 111],[58, 69, 85, 87, 99, 104, 127],[25, 27, 44],[62, 73, 101, 105, 120],[74, 85, 115],[3, 62, 73, 89, 91, 103, 108],[29, 31, 48],[66, 77, 105, 109, 124],[78, 89, 119],[7, 66, 77, 93, 95, 107, 112],[33, 35, 52],[0, 70, 81, 109, 113],[82, 93, 123],[11, 70, 81, 97, 99, 111, 116],[37, 39, 56],[4, 74, 85, 113, 117],[86, 97, 127],[15, 74, 85, 101, 103, 115, 120],[41, 43, 60],[8, 78, 89, 117, 121],[3, 90],[19, 78, 89, 105, 107, 119, 124],[45, 47, 64],[12, 82, 93, 121, 125],[7, 94],[0, 23, 82, 93, 109, 111, 123],[49, 51, 68],[1, 16, 86, 97, 125],[11, 98],[4, 27, 86, 97, 113, 115, 127],]
