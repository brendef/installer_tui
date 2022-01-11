class Server:
    def __init__(self):
        self._server

    @property
    def server(self):
         return self._server

    @server.setter
    def server(self, s):
        self._server = s

    # def ssh(self, host, user, pem):
    #     key = paramiko.RSAKey.from_private_key_file(pem)
    #     client = paramiko.SSHClient()
    #     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     client.connect(hostname=host, username=user, pkey=key)
    #     self.server = client

    # def execute_command(self, command):
    #     self.server.exec_command(command)
          