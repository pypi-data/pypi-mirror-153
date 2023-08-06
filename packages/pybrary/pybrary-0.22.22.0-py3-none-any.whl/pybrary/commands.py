import pybrary


def get_ip_adr():
    try:
        ok, adr = pybrary.get_ip_adr()
        if ok:
            return True, adr
        else:
            return False, f'Error ! {adr}'
    except Exception as x:
        return False, f'Exception ! {x}'


def bash(script):
    ret, out, err = pybrary.bash(script)
    ok = ret==0
    return ok, out if ok else f'\n > {out}\n ! {err}\n'


def ssh(host, cmd):
    ssh = pybrary.SSH()
    rem = ssh.hosts[host]
    ret, out, err = rem.run(cmd)
    return ret==0, out.strip()


def known_hosts():
    ssh = pybrary.SSH()
    ssh.hosts.known()
    return True, ''

