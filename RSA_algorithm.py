from random import randrange


class RSA:
    """
    Generates two keys - the public and the private one from passed prime numbers
    p and q. Each of two keys consists of two values. The public key
    consists of e and n, where e is a public exponent and n is RSA
    modulus. The private key consists of the same n and d which is a private
    exponent. RSA algorithm is a asymmetric cryptosystem, which allows
    to avoid key distribution problem unlike e.g. DES algorithm.
    """

    def __init__(self, prime_numbers):
        """
        Initialises two prime numbers p and q from the passed list 'prime_numbers',
        two empty lists to store the public and the private key and invokes 'generating_keys'
        in order to start generating keys.
        """
        self.p = prime_numbers[0]
        self.q = prime_numbers[1]
        self.public_key = []
        self.private_key = []
        self.generating_keys()

    def generating_keys(self):
        """
        Calculates modulus n for the public and private key, totient by Euler's totient
        functions. Invokes 'generating_e' in order to calculate public exponent e and
        'xgcd' in order to calculate private exponent d.
        """
        n = self.q * self.p
        totient = (self.q - 1) * (self.p - 1)
        e = self.generating_e(totient)

        gcd, x, y = self.xgcd(e, totient)

        if x < 0:
            d = x + totient
        else:
            d = x

        self.public_key.append(e)
        self.public_key.append(n)
        self.private_key.append(d)
        self.private_key.append(n)

    def generating_e(self, totient):
        """
        Generates a random number within the range 2 < e < totient and checks
        whether it is coprime with totient by invokes 'gcd'.
        """
        while True:
            e = randrange(2, totient)
            if self.gcd(e, totient) == 1:
                return e

    def gcd(self, a, b):
        """
        Performs the Eculidean algorithm using recursion.
        """
        if b == 0:
            return a
        else:
            return self.gcd(b, a % b)

    def xgcd(self, a, b):
        """
        Performs the extended Euclidean algorithm in order to calculates
        private exponent d.
        """
        x, old_x = 0, 1
        y, old_y = 1, 0

        while b != 0:
            quotient = a // b
            a, b = b, a - quotient * b
            old_x, x = x, old_x - quotient * x
            old_y, y = y, old_y - quotient * y

        return a, old_x, old_y
