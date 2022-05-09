import base64
import cmd
import json
import os
import sys

EOL = sys.platform == 'win32' and '\r\n' or '\n'


class Command:
    def __init__(self, command, properties, message):
        self.command = command
        self.properties = properties
        self.message = toCommadValue(message).replace(
            '%', '%25').replace('\r', '%0D').replace('\n', '%0A')

    def __str__(self):
        cmdStr = '::' + self.command
        _first = True
        for key, value in self.properties.items():
            if _first:
                _first = False
            else:
                cmdStr += ','
            cmdStr += key + '=' + value
        cmdStr += '::' + self.message
        return cmdStr


def toCommadValue(string):
    return string if type(string) == str else json.dumps(string)


def issueCommand(command, properties, message):
    print(str(Command(command, properties, message)))


def setSecret(secret):
    issueCommand('add-mask', {}, secret)

def main():
    token = sys.stdin.read()
    token = 'x-access-token:' + token
    token = base64.b64encode(token.encode('utf-8')).decode('utf-8')
    setSecret(token)
        
    knownHosts = os.path.join(os.path.expanduser('~'), '.ssh', 'known_hosts')
    with open(knownHosts, 'a') as f:
        f.write('''# Begin implicitly added github.com''' + EOL)
        f.write('''github.com ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==''' + EOL)
        f.write('''# End implicitly added github.com''' + EOL)
    
    os.system('git config --local --name-only --get-regexp core\.sshCommand')
    os.system('git submodule foreach --recursive git config --local --name-only --get-regexp \'core\.sshCommand\'')
    os.system('git config --local --unset-all \'core.sshCommand\'')
    os.system('git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader')
    os.system('git submodule foreach --recursive git config --local --name-only --get-regexp \'http\.https\:\/\/github\.com\/\.extraheader\'')
    os.system('git config --local --unset-all http.https://github.com/.extraheader')
    os.system(f'git config --local http.https://github.com/.extraheader AUTHORIZATION: basic {token}')

if __name__ == '__main__':
    main()