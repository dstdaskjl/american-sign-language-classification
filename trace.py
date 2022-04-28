import os
import sys
import time
import threading
import socket
from filelock import FileLock
from path import Path

path = Path()


# To control processes in a multi-computer system
class Trace:
    def __init__(self):
        self.keep_alive = True

    def start(self) -> None:
        self._terminate_duplicate_host()
        self.keep_alive = True
        self.update_liveness()
        threading.Thread(target=self._status, daemon=True).start()

    def end(self) -> None:
        self.keep_alive = False
        self.update_liveness()
        time.sleep(1)   # Let background thread die

    def update_liveness(self):
        host = socket.gethostname()
        pid = os.getpid()
        name = host + '_' + str(pid)

        with FileLock(path.var.alive_lock):
            if self.keep_alive:
                path.write(filepath=path.var.alive_filepath, content=name + '\n')
            else:
                contents = path.read(filepath=path.var.alive_filepath)
                path.create(path.var.alive_filepath)
                for content in contents:
                    if content[:len(name)] != name:
                        path.write(filepath=path.var.alive_filepath, content=content + '\n')

    def _terminate_duplicate_host(self):
        if self._host_exists():
            print('The host already exists')
            sys.exit(0)

    def _status(self) -> None:
        pid = os.getpid()
        while True:
            with FileLock(path.var.status_lock):
                status = path.read(filepath=path.var.status_filepath)[0]
                if status[:2] == path.var.dead:
                    self.keep_alive = False
            if not self.keep_alive:
                self.update_liveness()
                os.system('kill ' + str(pid))
            time.sleep(0.5)

    def _host_exists(self):
        current_host = socket.gethostname()
        hosts = path.read(filepath='Shared/alive.txt')
        for host in hosts:
            if current_host in host:
                return True
        return False
