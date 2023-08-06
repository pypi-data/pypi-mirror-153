from functools import reduce
from operator import mul

def prod(iter):
    return reduce(mul, iter, 1)