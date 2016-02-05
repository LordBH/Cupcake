from base64 import b64encode
from os import urandom

random_bytes = urandom(20)
token = b64encode(random_bytes).decode('utf-8')
a = ''
for x in token:
    if '/' == x:
        continue
    a += x

print(a[:-1])
