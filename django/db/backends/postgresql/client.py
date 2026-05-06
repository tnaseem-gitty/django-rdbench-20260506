import os
import signal
import subprocess

from django.db.backends.base.client import BaseDatabaseClient

def _escape_pgpass(txt):
    """
    Escape a fragment of a PostgreSQL .pgpass file.
    """
    return txt.replace('\\', '\\\\').replace(':', '\\:')


class DatabaseClient(BaseDatabaseClient):
    executable_name = 'psql'

    @classmethod
    def runshell_db(cls, conn_params):
        args = [cls.executable_name]

        host = conn_params.get('host', '')
        port = conn_params.get('port', '')
        dbname = conn_params.get('database', '')
        user = conn_params.get('user', '')
        passwd = conn_params.get('password', '')

        if user:
            args += ['-U', user]
        if host:
            args += ['-h', host]
        if port:
            args += ['-p', str(port)]
        args += [dbname]

        sigint_handler = signal.getsignal(signal.SIGINT)
        try:
            # Allow SIGINT to pass to psql to abort queries.
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            env = os.environ.copy()
            if passwd:
                env['PGPASSWORD'] = passwd
            subprocess.run(args, check=True, env=env)
        finally:
            # Restore the original SIGINT handler.
            signal.signal(signal.SIGINT, sigint_handler)
            if 'PGPASSWORD' in env:
                del env['PGPASSWORD']

    def runshell(self):
        DatabaseClient.runshell_db(self.connection.get_connection_params())
