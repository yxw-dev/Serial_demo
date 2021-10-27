import binascii

st = '55 00 02 D2 00 EC 24'
text = st.replace(' ' , '')
t2 = bytes.fromhex(text)
print(t2)
print(text)
t = binascii.unhexlify(str.encode(text))
print(t)
