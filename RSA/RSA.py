import os
import random

# ----- Utilites -----

def bytes_to_long(b):
    v = 0L
    for ch in b:
        v = (v << 8) | ord(ch)
    return v

def long_to_bytes(n):
    if n == 0:
        return '\x00'
    s = []
    while n > 0:
        s.append(chr(n & 0xff))
        n >>= 8
    return ''.join(reversed(s))

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def egcd(a, b):
    if b == 0:
        return (1, 0, a)
    x0, y0, g = egcd(b, a % b)
    return (y0, x0 - (a // b) * y0, g)

def modinv(a, m):
    x, y, g = egcd(a, m)
    if g != 1:
        return ValueError("modular inverse does not exist")
    return x % m

# ----- Miller-Rabin -----

def is_probable_prime(n, k=8):
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n % p == 0:
            return n == p
        
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for i in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for r in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True

def get_random_odd(bits):
    if bits < 2:
        return ValueError("Bits must be >= 2")
    byte_len = (bits + 7) // 8
    rnd = bytes_to_long(os.urandom(byte_len))
    rnd |= (1 << (bits - 1)) | 1
    return rnd

def generate_prime(bits, tries=1000):
    for _ in range(tries):
        p = get_random_odd(bits)
        if is_probable_prime(p):
            return p
    raise RuntimeError("Failed to generate prime after %d tries" % tries)

def generate_keypair(bits=512, e=65537):
    if bits < 16:
       raise ValueError("Bits too small")
    half = bits // 2
    while True:
        p = generate_prime(half)
        q = generate_prime(bits - half)
        if p == q:
            continue
        phi = (p - 1) * (q - 1)
        if gcd(e, phi) == 1:
            break
    n = p * q
    d = modinv(e, phi)
    pub = (n, e)
    priv = (n, d)
    return pub, priv 

def encrypt_bytes(msg_bytes, pub):
    n, e = pub
    m = bytes_to_long(msg_bytes)
    if m >= n:
        raise ValueError("Message too large for the key size; use smaller message or larger key")
    c = pow(m, e, n)
    return c

def decrypt_bytes(cipher_int, priv):
    n, d = priv
    m = pow(cipher_int, d, n)
    return long_to_bytes(m)

def encrypt(msg_str, pub):
    if isinstance(msg_str, unicode):
        msg_str = msg_str.encode('utf-8')
    return encrypt_bytes(msg_str, pub)

def decrypt_to_str(cipher_int, priv):
    b = decrypt_bytes(cipher_int, priv)
    return b

if __name__ == "__main__":
    pub, priv = generate_keypair(bits=512)
    n, e = pub
    msg = "hello RSA (py2)"
    print("Message", msg)
    c = encrypt(msg, pub)
    print("Ciphertext (int)", c)
    pt = decrypt_to_str(c, priv)
    print("Decrpted:", pt)

i = input()
