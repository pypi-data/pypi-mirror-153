import base64

# Take one of the DPS values 
text = 'CV4AAPoAAC0='
#text = 'CQYAB/oAAXQ=='
field = text.encode('ascii')
print("input text = %s" % text)

# Decode base64
z =base64.b64decode(field)
print("decoded = %r" % z)

# Convert to binary - 64 bits
zbin = "".join(["{:08b}".format(x) for x in z])
print("%s converts to %s" % (text, zbin))

# Assume 3 int values are in the 64 bits
a = zbin[:16]
b = zbin[16:40]
c = zbin[40:64]
print("----- 3 values -----")
print("V = %s = %0.1f V" % (a,int(a, 2)/10.0))
print("I = %s = %d mA" % (b,int(a, 2)))
print("P = %s = %d W" % (c,int(c, 2)))

