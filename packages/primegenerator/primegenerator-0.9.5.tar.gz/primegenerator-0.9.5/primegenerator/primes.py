from contextlib import contextmanager
from time import sleep
from bisect import bisect_left
from itertools import combinations_with_replacement
from .Operators import prod

def lcm(numbers):
    prime = primes()
    numbers = list(numbers) #otherwise first test numbers != old_numbers always returns true
    old_numbers=[]
    lcm = 1
    for p in prime:
        while True:
            old_numbers = numbers
            numbers = [n//p if n%p == 0 else n for n in numbers]
            if numbers != old_numbers:
                lcm *= p
            else:
                break
        if sum(numbers) == len(numbers):
            break
    return lcm

class primes(object):
    """Iterable object which yields prime numbers"""
    """Creates a cache of known primes which is accessed by all active instances"""
    """Each instance stores its last known position - so you can use it multiple times to get next prime, if this makes sense for you"""
    """"""
    """Can be initiated at any time with primes.preseed(n) to calculate all primes < n using sieve"""
    """Do this if you are sure you actually need that many primes"""
    """"""
    """Use startat1 = True if you want the first result to be 1"""
    """Maybe useful if you want p[i] to give i-th prime and 1 is the zero-th prime, 2 is 1st prime etc."""

    _knownprimes = [1,2,3,5,7]
    
    _lock = False

    _prime = None

    @classmethod
    def preseed(cls, seedsize):
        if cls._knownprimes[-1] >= seedsize:
            pass
        else:
            cls._knownprimes = [1]
            cls._knownprimes += cls.sieve(seedsize)
        return cls()

    def __init__(self, startat1 = False) -> None:
        cls = self.__class__
        if cls._prime == None:
            cls._prime = cls._generateprimes()
        self.i = -1
        if not startat1:
            self.i += 1
        
    def __eq__(self, __o: object) -> bool:
        return type(self) == type(__o) and self.i == __o.i

    def __iter__(self):
        return self

    def __next__(self):
        cls = self.__class__
        self.i += 1
        if self.i >= len(cls._knownprimes):
            next(cls._prime)
        return cls._knownprimes[self.i]

    @classmethod
    def _generateprimes(cls):
        #calculates potential primes using n = ak + j where:
        # a = product of first ai primes
        # k is integer 1, 2, ...
        # j is products of combinations 1, remaining primes > i-th prime; j < a
        # eg: for
        #   a = 2*3 = 6; j = (1,5); ai = 2
        #   a = 2*3*5 = 30; j = (1, 7, 9, 11, 13, 17, 19, 23, 29); ai = 3
        #   a = 2*3*5*7 = 210; j = (1, 11, 13, ..., 121 (11*11), 143 (11*13), 169, 187, 209(11*19)); ai = 4
        #
        #see: https://math.stackexchange.com/questions/616093/why-every-prime-3-is-represented-as-6k-pm1
        
        primeproducts = cls._endless_primeproducts()
        
        while True:
            for a, primefactors, next_a in primeproducts:
                kj = cls._loop_kj(a, primefactors)
                for k, j in kj:
                    n = a*k + j
                    if n > next_a: break #time for a new a
                    if n <= cls._knownprimes[-1]: continue #fast forward - next k, j
                    for p in cls._knownprimes[1:]: #not outsourcing this to an isprime() function due to 10% performance cost!
                        if n%p == 0: #divisible by p -> not prime
                            break #for p in cls.knownprimes[1:]
                        elif p*p > n: #faster than sqrt(n)
                            cls._knownprimes.append(n) #no prime factor -> is prime
                            yield
                            break #for p in cls.knownprimes[1:]

    @classmethod
    def _endless_primeproducts(cls):
        a, i = 1, 0
        while a <= cls._knownprimes[-1] + 1: #fast forward values for knownprimes - go one step too far
            i += 1
            a *= cls._knownprimes[i]
        a = a // cls._knownprimes[i] # then rewind
        i -= 1
        yield a, cls._knownprimes[1:i+1], a * cls._knownprimes[i+1] #phew - got the current numbers for highest known prime
        while True:
            i += 1
            a *= cls._knownprimes[i]
            yield a, cls._knownprimes[1:i+1], a * cls._knownprimes[i+1]

    @classmethod
    def _loop_kj(cls, a, primefactors):
        possible_j = cls._get_possiblej(a, primefactors)
        k = 1
        while True:
            for j in possible_j: 
                yield k, j
            k += 1
   
    @classmethod
    def _get_possiblej(cls, a, primefactors):
        possible_j = [p for p in cls._knownprimes if p not in primefactors and p < a]
        n = 1
        max_p = a//(possible_j[1] ** n)
        while max_p >= possible_j[1]:
            if max_p in possible_j:
                mi = possible_j.index(max_p)
            else:
                mi = bisect_left(possible_j, max_p)
            possible_j += [prod(ps) for ps in combinations_with_replacement([p for p in possible_j[1:mi+1]],n+1)]
            n += 1
            max_p = a//(possible_j[1] ** n)
        if n > 1:
            possible_j = tuple(sorted([p for p in possible_j if p < a]))
        return possible_j

    @classmethod
    @contextmanager
    def test_wrapper(cls):
        while cls._lock:
            sleep(1)
        cls._lock = True

        cls._prime = cls._generateprimes()
        cls._knownprimes = [1,2,3,5,7]

        yield

        cls._prime = cls._generateprimes()
        cls._knownprimes = [1,2,3,5,7]
        cls._lock = False

    @staticmethod
    def sieve(n):
    #https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n/3035188#3035188 (primes1)
    # Returns a list of primes < n
        n = int(n)
        sieve = [True] * (n//2)
        for i in range(3,int(n**0.5)+1,2):
            if sieve[i//2]:
                sieve[i*i//2::i] = [False] * ((n-i*i-1)//(2*i)+1)
        return [2] + [2*i+1 for i in range(1,n//2) if sieve[i]]         
  