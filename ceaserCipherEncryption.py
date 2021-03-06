import pyperclip

message = 'DZ XLYj aPZaWP WTgP hTeSTY fYSLaaj NTcNfXdeLYNPd LYO jPe hTWW YZe eLVP eSP TYTeTLeTgP eZ NSLYRP eSPTc dTefLeTZY MPNLfdP eSPj LcP NZYOTeTZYPO eZ L WTQP ZQ dPNfcTej, NZYQZcXTej, LYO NZYdPcgLeTZY, LWW ZQ hSTNS XLj LaaPLc eZ RTgP ZYP aPLNP ZQ XTYO, Mfe TY cPLWTej, YZeSTYR Td XZcP OLXLRTYR eZ eSP LOgPYefcZfd daTcTe'
key = 15
mode = 'decrypt'
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!?'
translated = ''

for symbol in message:
    if symbol in SYMBOLS:
        symbolIndex = SYMBOLS.find(symbol)
        
        if mode == 'encrypt':
            translatedIndex = symbolIndex + key
            
        elif mode == 'decrypt':
            translatedIndex = symbolIndex - key
            
        if translatedIndex >= len(SYMBOLS):
            translatedIndex = translatedIndex - len(SYMBOLS)
            
        elif translatedIndex <= 0:
            translatedIndex = translatedIndex + len(SYMBOLS)
            
        translated = translated + SYMBOLS[translatedIndex]
    else:
        translated = translated + symbol
    
print(translated)
