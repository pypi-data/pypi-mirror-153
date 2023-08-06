from os import scandir
from pathlib import Path

from .files import grep
from .shell import bash
from .commandparams import Param, ValidationError


class Config:
    def __init__(self, ssh):
        self.ssh = ssh

    def parse(self, path='~/.ssh'):
        rex = r"\s*(?<!#)(\w+)(?:\s*=\s*|\s+)(.+)"
        hosts, host = dict(), None
        path = Path(path).expanduser()
        for cfg in scandir(path):
            if cfg.is_file and cfg.name.endswith('.cfg') and 'Host' in open(cfg).read():
                for k, v in grep(cfg, rex):
                    key = k.lower()
                    value = v.strip('"')
                    if key == "host":
                        if host:
                            hosts[host] = items
                        host = value
                        items = dict()
                    else:
                        if key in ('identityfile', 'localforward', 'remoteforward'):
                            items.setdefault(key, []).append(value)
                        else:
                            items[key] = value
                hosts[host] = items
        return hosts.items()


class Host:
    def __init__(self, ssh, name, data, shell=bash):
        self.ssh = ssh
        self.name = name
        self.data = data
        for key, val in data.items():
            setattr(self, key, val)
        self.shell = shell

    @property
    def adr(self):
        return self.hostname

    @property
    def key(self):
        return self.identityfile[0]

    def run(self, cmd, timeout=None):
        timeout = timeout or self.ssh.timeout
        return self.shell(f'''
            ssh {self.name} -o ConnectTimeout={timeout} -t {cmd}
        ''')

    def __call__(self, cmd):
        ret, out, err = self.run(cmd)
        return ret==0 and out or f'\n ! {out.strip()}\n'

    @property
    def host(self):
        return self('hostname')

    def ping(self):
        ret, out, err = self.shell(f'''
            ping -c 1 {self.hostname}
        ''')
        return ret==0

    def is_known(self):
        ret, out, err = self.shell(f'''
            ssh-keygen -F {self.hostname}
        ''')
        return ret==0

    def unknown(self):
        return self.shell(f'''
            ssh-keygen -R {self.hostname}
        ''')

    def known(self):
        if self.is_known(): return
        if not self.ping(): return
        print(f'known {self.hostname}')
        return self.shell(f'''
            touch ~/.ssh/known_hosts
            ssh-keyscan -H {self.hostname} >> ~/.ssh/known_hosts
        ''')

    def port(self, port):
        return self.shell(f'''
            ssh  -Nf -L {port}:localhost:{port} {self.name}
        ''')

    def get(self, rem, loc=None):
        return self.shell(f'''
            scp {self.name}:{rem} {loc or rem})
        ''')

    def put(self, loc, rem=None):
        return self.shell(f'''
            scp {loc} {self.name}:{rem or loc})
        ''')

    @property
    def mountpoint(self):
        return f'{self.ssh.mountpoint}/{self.name}'

    def mount(self, rem):
        loc = f'{self.mountpoint}/{rem}'
        return self.shell(f'''
            mkdir -p {loc}
            sshfs {self.name}:{rem} {loc}
        ''')

    def umount(self, loc):
        loc = f'{self.mountpoint}/{loc}'
        return self.shell(f'''
            fusermount -u {loc}
        ''')

    def sync(self, loc, rem=None, delete=True, exclude=None, dry=True):
        option = "--dry-run" if dry else "--progress"
        exclude = exclude or self.ssh.exclude
        exclude = f'--exclude-from={exclude}' if exclude else ''
        delete = '--delete' if delete else ''
        self(
            f'mkdir -p {rem}'
        )
        return self.shell(f'''
            rsync -crzhiv {exclude} {delete} {option} -e "ssh -i {self.key}" {loc} {self.user}@{self.adr}:{rem or loc}
        ''')

    def restore(self, rem, loc=None, delete=True, exclude=None, dry=True):
        option = "--dry-run" if dry else "--progress"
        exclude = exclude or self.ssh.exclude
        exclude = f'--exclude-from={exclude}' if exclude else ''
        delete = '--delete' if delete else ''
        self.shell(
            f'mkdir -p {loc}'
        )
        return self.shell(f'''
            rsync -crzhiv {exclude} {delete} {option} -e "ssh -i {self.key}" {self.user}@{self.adr}:{rem} {loc or rem}
        ''')

    def __str__(self):
        return f'\n{self.name}:\n'+'\n'.join(
            f'\t{k} = {v}' for k, v in self.data.items()
        )


class Hosts:
    def __init__(self, ssh):
        self.ssh = ssh
        self.all = dict()
        for name, items in ssh.config.parse():
            host = Host(ssh, name, items)
            setattr(self, name, host)
            self.all[name] = host

    def known(self):
        done = set()
        for host in self:
            if host.hostname in done: continue
            host.known()
            done.add(host.hostname)

    def __iter__(self):
        return iter(self.all.values())

    def __getitem__(self, name):
        return self.all.get(name)

    def __str__(self):
        return '\n'+'\n'.join(map(str,self.all.values()))


class SSH:
    def __init__(self, **k):
        self.mountpoint = k.get('mountpoint', '/tmp/ssh')
        self.exclude = k.get('exclude')
        self.timeout = k.get('timeout', 3)
        self.config = Config(self)
        self.hosts = Hosts(self)


class ParamSSH(Param):
    name = 'SSH Host'

    def verify(self, value):
        ssh = SSH()
        host = ssh.hosts[value]
        if host:
            return host
        else:
            raise ValidationError(f'"{self.name}" unknown SSH host : {value}')
