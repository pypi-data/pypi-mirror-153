from functools import partial
from subprocess import (
    PIPE,
    CalledProcessError,
    run,
)


def shell(script, shell):
    try:
        proc = run(
            script,
            stdout = PIPE,
            stderr = PIPE,
            check  = True,
            shell  = True,
            executable = shell,
        )
    except CalledProcessError as exc:
        ret = exc.returncode
        out = exc.stdout.decode('utf-8')
        err = exc.stderr.decode('utf-8')
    else:
        ret = proc.returncode
        out = proc.stdout.decode('utf-8').strip()
        err = proc.stderr.decode('utf-8').strip()
    return ret, out, err


bash = partial(shell, shell='/bin/bash')
