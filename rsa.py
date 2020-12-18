import math
import primesieve
import random

def RSA(p, q):
    n = p * q;
    z = (p - 1) * (q - 1);
    print("z =", z)
    e = 0
    for i in range(2, z):
        if math.gcd(i, z) == 1:
            e = i
            print('e =',i)
            break
    d = 0
    for i in range(z):
        x = 1+(i*z)
        if x % e == 0:
            d = int(x / e);
            break;
    print('d =', d)
    return [e, n], [d, n]


def encrypt(message, public_key):
    encrypt_message = []
    for m in message:
        encrypt_message.append(pow(ord(m), public_key[0])% public_key[1])
    return encrypt_message


def decrypt(message, private_key):
    decrypt_message = ''
    for m in message:
        decrypt_message += chr(pow(m, private_key[0]) % private_key[1])
    return decrypt_message


p = primesieve.nth_prime(random.randint(50, 150))#457
q = primesieve.nth_prime(random.randint(50, 150))#1213
public_key, private_key = RSA(p, q)
print('public_key', public_key)
print('private_key', private_key)
msg = encrypt('The owls are not what they seem', public_key)
print('Message:', decrypt(msg, private_key))