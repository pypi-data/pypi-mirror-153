# Introduction 
Fast `PrimeNumbers` generator which caches previous results across instances.\
You usually don't need as many primes as the worst-case - eg for the included `lcm` (lowest common multiplier) function.

Also provides a very fast `primesieve` if you wish to pre-calculate a large number of primes.

# Getting Started
Installation: `pip install primegenerator`

## Main usage:
```python
from primegenerator import PrimeNumbers
primes = PrimeNumbers()
for prime in primes:
    ... #do something
    if ... #beware this is an infinite iterator!
        break
```

## Test if number is prime:
```python
from primegenerator import PrimeNumbers
assert 5 in PrimeNumbers()
assert 9 not in PrimeNumbers()
```


## Preseed - if you know you need all primes up to n:
```python
from primegenerator import PrimeNumbers
n = 100 #somebignumber
primes = PrimeNumbers.preseed(n)
for prime in primes:
    ... #do something
    if ... #beware this is still an infinite iterator and will keep going past the seed point!
        break
```

## Lowest common multiplier:
```python
from primegenerator import lcm
numbers = [2,3,4]
assert lcm(numbers) == 12
assert lcm(3,4,5) == 60
```

## Sieve:
```python
from primegenerator import primesieve
listofprimes = primesieve(maxprime)
```

# Build and Test
Tests are written for pytest in `/tests/test_*.py`\
`pip -r tests/requirements.txt` for additional imports required for some tests.\
Tests are available on the ADO repository (see link below)

`/dev` contains some useful stuff for debugging, profiling and further development and is only available on the ADO repository (see link below)

# Contribute
Code repository (ADO): https://dev.azure.com/MusicalNinjas/MikesMath/_git/primes \
Homepage: https://dev.azure.com/MusicalNinjas/MikesMath

# Coming soon...
```python
assert primes[3] == 5
```