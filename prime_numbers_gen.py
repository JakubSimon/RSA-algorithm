from random import randrange


class PrimeNumGen:
    """
    Generates large prime numbers with a high level
    of probability. Uses division with all primes lower
    than 1000 and Rabin-Miller primality test.
    """

    def __init__(self, prime_size):
        """
        Initialises the size of prime number (expressed in bits),
        list of prime numbers lower than 1000,
        empty list to store generated prime numbers
        and invokes 'generating' to generate two prime numbers
        of the determined size.
        """
        self.prime_size = prime_size
        self.low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                           47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                           103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
                           157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                           211, 223, 227, 229, 233, 239, 241, 251, 257, 263,
                           269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                           331, 337, 347, 349, 353, 359, 367, 373, 379, 383,
                           389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                           449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
                           509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                           587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
                           643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                           709, 719, 727, 733, 739, 743, 751, 757, 761, 769,
                           773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                           853, 857, 859, 863, 877, 881, 883, 887, 907, 911,
                           919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                           991, 997]
        self.prime_numbers = []
        self.generating()

    def generating(self):
        """
        Invokes 'gen_rand_num' until two prime numbers are generated
        """
        while len(self.prime_numbers) < 2:
            self.prime_numbers.append(self.gen_rand_num())

    def gen_rand_num(self):
        """
        Generates odd random numbers between the range 2^(prime_size - 1) + 1 and
        2^(prime_size) - 1. Next invokes 'low_level_test' if passes then
        invokes 'miller_rabin_test', if also passes returns prime number and adds
        to the list 'prime_numbers'.
        """
        while True:
            prime_candidate = randrange(2**(self.prime_size - 1) + 1, 2**self.prime_size - 1, 2)
            if self.low_level_test(prime_candidate):
                if self.miller_rabin_test(prime_candidate):
                    return prime_candidate

    def low_level_test(self, test_num):
        """
        Divides the generated number by all prime numbers under 1000 and checks
        whether the generated number is divisible by those numbers, if not the
        generated number is initially prime.
        """
        if test_num < 2:
            return False
        for divisor in self.low_primes:
            if test_num % divisor == 0 and divisor < test_num:
                return False
        return True

    def miller_rabin_test(self, test_num):
        """
        Performs Miller-Rabin test in order to check the primality
        of the number with high probability. If test passes, it means that
        test number is prime with the probability of 4^(-num_of_test).
        """
        num_of_tests = 20
        s = 0
        d = test_num - 1
        while d % 2 == 0:
            d //= 2
            s += 1

        for num_of_test in range(num_of_tests):
            a = randrange(2, test_num - 1)
            v = pow(a, d, test_num)
            if v == 1:
                return True
            i = 0
            while v != (test_num - 1):
                if i == s - 1:
                    return False
                else:
                    i += 1
                    v = (v**2) % test_num
            return True
