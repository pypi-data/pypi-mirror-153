from urllib.request import urlopen
from ipaddress import ip_address, IPv4Address

from .shell import shell
from .commandparams import Param, ValidationError
from . import logger, debug, error


def get_ip_adr():
    url = 'http://api.ipify.org'
    with urlopen(url, timeout=1) as resp:
        if resp.status==200:
            adr = resp.read().decode().strip()
            debug('ip adr : %s', adr)
            return True, adr
        else:
            error('%s %s', resp.status, resp.reason)
            return False, resp.reason


class ParamIPv4(Param):
    name = 'IPv4 adr'

    def verify(self, value):
        try:
            adr = ip_address(value)
            if not isinstance(adr, IPv4Address):
                raise ValueError
            return adr
        except ValueError:
            raise ValidationError(f'{value} is not IPv4')

