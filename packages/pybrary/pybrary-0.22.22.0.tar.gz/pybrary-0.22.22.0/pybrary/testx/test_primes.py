from pytest import raises

from pybrary.primes import primes


def test_n_contains():
    assert 0 not in primes
    assert 1 not in primes
    assert 2 in primes
    assert 3 in primes
    assert 4 not in primes
    assert 5 in primes
    assert 6 not in primes
    assert 7 in primes
    assert 8 not in primes
    assert 9 not in primes
    assert 11159 in primes


def test_n_iter():
    expected = 2,3,5,7,11,13,17,19,23
    for e, p in zip(expected, primes):
        assert p == e

def test_n_iindex():
    assert primes[0] == 2
    assert primes[1] == 3
    assert primes[2] == 5
    assert primes[3] == 7

def test_c_index_error():
    with  raises(OverflowError):
        primes[-1]

def test_n_decomp():
    assert primes.factors(12) == [2, 2, 3]
    assert primes.factors(15) == [3, 5]
    assert primes.factors(179) == [179]
    assert primes.factors(1) == []
    assert primes.factors(2**9) == [2 for _ in range(9)]
    assert primes.factors(7**7) == [7 for _ in range(7)]


if __name__=='__main__':
    from pytest import main
    main(['-v', '-s'])
