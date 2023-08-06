class Primes:
    def __init__(self):
        self.primes = [3]
        '''
        self.primes = array('L', [3]) # ! bigger and slower !
        '''

    def next(self):
        primes = self.primes
        n = primes[-1]
        while True:
            n+=2
            for i in primes:
                if n%i==0:
                    break
            else:
                primes.append(n)
                return n

    def __getitem__(self, i):
        if i<0: raise OverflowError
        if i==0: return 2
        primes = self.primes
        nxt = self.next
        while len(primes)<i: nxt()
        return primes[i-1]

    def __iter__(self):
        yield 2
        for p in self.primes:
            yield p
        while True:
            yield self.next()

    def __contains__(self, num):
        if num>2:
            if num%2==0: return False
        else:
            return num==2
        last = int(num**.5)
        for p in self:
            if num==p: return True
            if num%p==0: return False
            if p>last: return True

    def factors(self, num):
        if num<2: return []
        last = int(num**.5)
        for p in self:
            if num==p: return [num]
            if num % p == 0:
                return [p] + self.factors(num//p)
            if p>last: return [num]


primes = Primes()

