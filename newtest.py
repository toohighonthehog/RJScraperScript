x1 = 1234.56

print (str(x1))
b =  str(x1).encode()

print (b)

x2 = int(b.decode())

print (type(x2))
print (x2)