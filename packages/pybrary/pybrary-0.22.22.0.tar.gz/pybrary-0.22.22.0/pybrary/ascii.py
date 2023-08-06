from re import compile as rec
from functools import partial


# remove ansi codes
rm_ansi_codes = partial(rec(
    r'\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK](\x0F)?'
).sub, '')


# Convert file permissions from str to oct
def oct_mod(str_mod):
    assert len(str_mod)==9, f'bad mode : {str_mod} ({len(str_mod)})'

    def digit(str_bits):
        assert len(str_bits)==3, f'bad bits : {str_bits}'
        value = sum(
            2**i if c!='-' else 0
            for i, c in enumerate(str_bits[::-1])
        )
        return str(value)

    digits = [
        digit(str_mod[i*3:i*3+3])
        for i in range(3)
    ]

    return  ''.join(digits)

