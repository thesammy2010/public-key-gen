import time

from typing import Dict, Any
from Crypto.PublicKey import RSA


class PrimeNumberException(Exception):
    pass


class IterationException(Exception):
    pass


class IntegerException(Exception):
    pass


class NegativeNumbersException(Exception):
    pass


class QuotientException(Exception):
    pass


class TooSmallException(Exception):
    pass


class SameNumberException(Exception):
    pass


class TypeException(Exception):
    pass


def greatest_common_divisor(a: int = 0, b: int = 0) -> (int, int, bool):
    if not isinstance(a, int) or not isinstance(b, int):
        raise IntegerException("a and b must both be integers. A = %s, B =%s" % (a, b))

    if a == 0 and b == 0:
        return 0, 0, True
    if a == 0:
        return b, 0, True
    if b == 0:
        return a, 0, True

    if a >= b:
        p: int = a
        q: int = b
    else:
        p: int = b
        q: int = a

    r: int = p % q
    s: float = (p - r) / q

    if not s == int(s):
        raise QuotientException(f"Quotient equation error: [{p}, {q}] --> [({p})({s}) + {r} , {q}]")

    return q, r, False


def calculate_encryption_value(m: int) -> int:

    for i in range(2, 65537):

        res: bool = False
        a: int = i
        b: int = m
        while res is False:
            a, b, res = greatest_common_divisor(a=a, b=b)

        if a == 1:
            return i

    raise IterationException("Timed out calculating decryption value. Try picking a smaller number")


def calculate_decryption_value(e: int, m: int) -> int:
    i: int = 1
    t: float = time.time()
    # while i < 65537:
    while time.time() - t < 10:
        if (e * i) % m == 1:
            return i
        else:
            i += 1
    raise IterationException("Timed out calculating decryption value. Try picking a smaller number")


def check_input(p: int, q: int) -> None:

    for i, j in locals().items():

        if j is None:
            raise TypeException(f"{i} is of type {type(j)}, must be of type int")

        for n in range(2, j):
            if j % n == 0:
                raise PrimeNumberException(f"{i} is not a prime number")
        if int(j) != j:
            raise IntegerException(f"{i} is not an Integer")
        if j < 0:
            raise NegativeNumbersException(f"{i} cannot be negative")
        if j < 5:
            raise TooSmallException(f"{i} is too small. Choose a number larger than 10")

    if p == q:
        raise SameNumberException("Numbers cannot be the same")


def construct_public_key(n: int, e: int, d: int) -> str:

    key = RSA.construct(rsa_components=(n, e, d))
    pub: str = key.exportKey(format="OpenSSH").decode()
    return pub


def construct_private_key(n: int, e: int, d: int) -> str:

    key = RSA.construct(rsa_components=(n, e, d))
    pub: str = key.exportKey().decode()
    return pub


def generate(**kwargs: Dict[str, Any]) -> Dict[str, int]:
    # expected_json = {"p": 10, "q": 20, "use_default_encryption": False}

    p: int = kwargs.get("p")
    q: int = kwargs.get("q")
    check_input(p=p, q=q)

    n: int = p * q
    m: int = (p - 1) * (q - 1)

    e: int = calculate_encryption_value(m=m)
    d: int = calculate_decryption_value(e=e, m=m)

    pub: str = construct_public_key(n=n, e=e, d=d)
    pri: str = construct_private_key(n=n, e=e, d=d)

    return {"encryption_key (E)": e, "modulus (N)": n, "public_key": pub, "private_key": pri}


def encrypt(message: int, encryption_key: int, modulus: int) -> Dict[str, int]:
    locals()["encrypted_message"] = (message ** encryption_key) % modulus
    return locals()


def decrypt(encrypted_message: int, decryption_key: int, modulus: int) -> Dict[str, int]:
    response: Dict[str, int] = locals()
    response["decrypted_message"] = (encrypted_message ** decryption_key) % modulus
    del response["decryption_key"]  # this is the private key
    return response





