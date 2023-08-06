# coding=utf-8
# pylint: disable=redefined-builtin
import os
import threading
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from utils.system import get_root_path


class MyHandler(FTPHandler):

    def on_connect(self):
        print("%s:%s connected" % (self.remote_ip, self.remote_port))

    def on_disconnect(self):
        # do something when client disconnects
        pass

    def on_login(self, username):
        # do something when user login
        pass

    def on_logout(self, username):
        # do something when user logs out
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        print(self.username, file)

    def on_file_received(self, file):
        # do something when a file has been received
        print(self.username, file)

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        print(self.username, file)

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        os.remove(file)


def start_ftp_server():
    working_path = os.environ["working_path"]
    home_dir = os.path.join(working_path, "fw_bin")
    if os.path.exists(home_dir) is False:
        os.mkdir(home_dir)
    authorizer = DummyAuthorizer()
    authorizer.add_user('ftp_user', 'Cnex!321', homedir=home_dir, perm='elw')
    authorizer.add_anonymous(homedir=home_dir)
    handler = MyHandler
    handler.authorizer = authorizer
    try:
        server = FTPServer(('0.0.0.0', 10021), handler)
        server.serve_forever()
        print("FTP server start succeed.")
    except Exception as all_exception:
        print("FTP server already start.")


def thread_start_ftp_server():
    thread_p = threading.Thread(target=start_ftp_server)
    thread_p.setDaemon(True)
    thread_p.start()


if __name__ == "__main__":
    thread_start_ftp_server()
