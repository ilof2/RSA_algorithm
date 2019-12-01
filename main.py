import random


class RSA:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = None
        self.e = 2**16+1
        self.F = None

    @staticmethod
    def _gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def is_prime(self, num):
        if num == 2:
            return True
        if num < 2 or num % 2 == 0:
            return False
        for n in range(3, int(num ** 0.5) + 2, 2):
            if num % n == 0:
                return False
        return True

    def mmi(self, e, phi):
        """So slow and unreliable realization of MMI"""
        i = 1
        while True:
            c = phi * i + 1
            if c % e == 0:
                c /= e
                break
            i += 1
        return c

    def gen_keys(self):
        expr = all([self.is_prime(self.p), self.is_prime(self.q)])
        if self._gcd(self.p, self.q) != 1 or not expr:
            raise ValueError("Numbers are not coprime")
        self.n = self.p * self.q
        self.F = (self.p - 1) * (self.q - 1)
        print("Phi", self.F)

        # This is fast mmi realization but not beautiful. I will rewrite her later
        mmi = lambda A, n, s=1, t=0, N=0: (n < 2 and t % N or mmi(n, A % n, t, s - A // n * t, N or n), -1)[n < 1]

        d = int(mmi(self.e, self.F))
        print(d)
        return {"pub": (self.n, self.e), "priv": (d, self.n)}

    @staticmethod
    def encode(pub_key: tuple, init_msg: str):
        encoded = [pow(ord(char), pub_key[1], pub_key[0]) for char in init_msg]
        return encoded

    @staticmethod
    def decode(private_key: tuple, encoded_msg: list):
        char_list = [chr(pow(char, private_key[0], private_key[1]))for char in encoded_msg]
        return ''.join(char_list)


if __name__ == "__main__":
    p = input("Firsts prime number: ")
    q = input("Second prime number (Should be coprime with first): ")
    rsa = RSA(int(p), int(q))
    keys = rsa.gen_keys()
    print(keys)
    message = input("Your digit message: ")
    enc_m = rsa.encode(keys["pub"], message)
    dec_m = rsa.decode(keys["priv"], enc_m)
    print(f"Initial message {message}\nEncoded message: {enc_m}\nDecoded message: {dec_m}")
