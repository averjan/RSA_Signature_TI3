# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class PrivateKey:
    def __init__(self, d, r):
        self.d = d
        self.r = r


class PublicKey:
    def __init__(self, e, r):
        self.e = e
        self.r = r


alphabet_start = ord(' ')


def is_prime(num):
    if num > 1:
        for i in range(2, num):
            if num % i == 0:
                return False

    return True


def are_relatively_prime(a, b):
    for i in range(2, min(a, b) + 1):
        if (a % i == 0) and (b % i == 0):
            return False
    return True


def euclide(a, b):
    d0, d1 = a, b
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while d1 > 1:
        q = d0 // d1
        d2 = d0 % d1
        x2 = x0 - (q * x1)
        y2 = y0 - (q * y1)
        d0, d1 = d1, d2
        x0, x1 = x1, x2
        y0, y1 = y1, y2

    return x1, y1, d1


def need_more_size(msg, r):
    for c in msg:
        if ord(c) - alphabet_start >= r:
            print("Message requires key longer")
            return True

    return False


def get_pq():
    p = q = 0
    while p == q:
        p = int(input("Enter p value: "))
        while not is_prime(p):
            print("p must be prime")
            p = int(input("Enter p value: "))

        q = int(input("Enter q value: "))
        while not is_prime(q):
            print("q must be prime")
            q = int(input("Enter q value: "))

    return p, q


def create_key_pair(msg):
    p, q = get_pq()
    r = p * q
    while need_more_size(msg, r):
        p, q = get_pq()
        r = p * q

    x = (p - 1) * (q - 1)
    e = 2
    for i in range(3, x, 2):
        if are_relatively_prime(i, x):
            e = i
            break

    temp_x, d, nod = euclide(x, e)
    if d < 0:
        d += x

    return PublicKey(e, r), PrivateKey(d, r)


def get_hash(msg):
    h = 100
    p, q = get_pq()
    n = p * q
    for c in msg:
        h = pow(h + ord(c) - alphabet_start, 2) % n

    return h


def create_digital_signature(m_code, key):
    return pow(m_code, key.d) % key.r


def reverse_digital_signature(s_code, key):
    return pow(s_code, key.e) % key.r


# MAIN
message = input("Enter the message")
public_key, private_key = create_key_pair(message)
m = get_hash(message)
s = create_digital_signature(m, private_key)

m2 = reverse_digital_signature(s, public_key)
m_extra_hash = get_hash(message)
print(m2 == m_extra_hash)
