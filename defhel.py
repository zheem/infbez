import primesieve
import random


class User:
    def __init__(self, secret_num, p, g):
        self.p = p
        self.g = g
        self.secret_num = secret_num
        self.key = pow(g, secret_num) % p

    def get_key(self):
        return self.key

    def get_secret_key(self, companion_key):
        return pow(companion_key, self.secret_num) % self.p


g = primesieve.nth_prime(random.randint(50, 150))
p = primesieve.nth_prime(random.randint(50, 150))
Jhon = User(random.randint(1, 500), p, g)
Mentos = User(random.randint(1, 500), p, g)
print('Jhon key:', Jhon.get_secret_key(Mentos.get_key()))
print('Mentos key:', Mentos.get_secret_key(Jhon.get_key()))