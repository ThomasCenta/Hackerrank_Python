def _shiftLeft(arr):
    for i in range(len(arr)-1):
        arr[i] = arr[i+1]

def positiveMod(n, mod):
    n = n % mod
    if n < 0:
        n += mod
    return n

def modularInverse(n, mod):
    n = positiveMod(n, mod)
    if (n == 1):
        return 1
    pSeries = [0, 1, 0]
    quotients = [0, 0, 0]
    remainders = [0, 0, 0]
    quotients[0] = mod // n
    remainders[0] = mod % n
    if (remainders[0] == 0):
        return -1
    quotients[1] = n // remainders[0]
    remainders[1] = n % remainders[0]
    pSeries[2] = (pSeries[0] - (pSeries[1] * quotients[0] % mod)) % mod
    if (remainders[1] == 0):
        return pSeries[2]
    remainders[2] = remainders[0] % remainders[1]
    quotients[2] = remainders[0] // remainders[1]
    while (remainders[2] != 0):
        _shiftLeft(remainders)
        _shiftLeft(quotients)
        _shiftLeft(pSeries)
        remainders[2] = remainders[0] % remainders[1]
        quotients[2] = remainders[0] // remainders[1]
        pSeries[2] = (pSeries[0] - (pSeries[1] * quotients[0] % mod)) % mod
    if (remainders[1] != 1):
        return -1
    return (pSeries[1] - (pSeries[2] * quotients[1] % mod)) % mod

def modDivide(i, j, mod):
    return i * modularInverse(j, mod) % mod

def powMod(a, b, mod):
    if b == 0:
        return 1
    temp = powMod(a, b//2)
    if b % 2 == 0:
        return temp*temp % mod
    else:
        return a*temp*temp % mod
