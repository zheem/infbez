import primesieve
import hashlib
import random


def hash_generation(*args):
    a = ''.join(str(a) for a in args)
    return int(hashlib.sha256(a.encode('utf-8')).hexdigest(), 16)


def rand_generation(bits_num):
    return random.SystemRandom().getrandbits(bits_num)


def prime_check(n):
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n and n % d != 0:
        d += 2
    return d * d > n


def generator(N):
    X = N - 1
    for x in range(1, X):
        for g in range(1, X):
            if pow(g, x, N) == X:
                return g


def authentication(N, g, k, I, p, s, x, v):
    a = 0
    A = 0
    while A == 0:
        a = rand_generation(1025)
        A = pow(g, a, N)

    b = 0
    B = 0
    while B == 0:
        b = rand_generation(1024)
        B = (k * v + pow(g, b, N)) % N

    u = hash_generation(A, B)
    if u == 0:
        print('u == 0, connection interrupted')
        return -1

    x = hash_generation(s, p)
    S_client = pow(B - k * pow(g, x, N), a + u * x, N)
    K_client = hash_generation(S_client)

    S_server = pow(A * pow(v, u, N), b, N)
    K_server = hash_generation(S_server)

    print('\nK_server =',K_server)
    print('K_client =',K_client)

    М_client = hash_generation(hash_generation(N) ^ hash_generation(g), hash_generation(I), s, A, B, K_client)
    М_server = hash_generation(hash_generation(N) ^ hash_generation(g), hash_generation(I), s, A, B, K_server)
    if М_server == М_client:
        print('\nМ_client == М_server')
        print(М_server, М_client)
    else:
        print('\nМ_client != М_server')
        return -1

    R_server = hash_generation(A, М_client, K_server)
    R_client = hash_generation(A, М_client, K_client)
    if R_server == R_client:
        print('R_server == R_client')
        print(R_server, R_client)
        return 1
    else:
        print('R_server != R_client')
        return -1


N = primesieve.nth_prime(random.randint(10, 100))
while True:
    if prime_check((N - 1) // 2):
        break
    N = primesieve.nth_prime(random.randint(10, 100))
print('N =', N)

g = generator(N)
print('g =', g)

k = hash_generation(N, g)
print('k =', k)

I = 'Username'
p = '123456789'
s = rand_generation(64)
x = hash_generation(s, p)
v = pow(g, x, N)

authentication(N, g, k, I, p, s, x, v)