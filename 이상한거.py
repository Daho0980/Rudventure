a = 0
b = 1
c = 2
d = {'a' : a, 'b' : b, 'c' : c}
e = {'d' : d}
print(a)
exec("a += c", d)
a = d['a']
print(a)
print(eval("d['a']", e))