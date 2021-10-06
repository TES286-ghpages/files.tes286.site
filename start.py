import os


with open('/etc/resolv.conf', 'w') as fd:
    fd.write('''\
search blue.kundencontroller.de
options rotate
nameserver 2001:67c:2b0::4
nameserver 2001:67c:2b0::6
#nameserver 2001:4860:4860::6464
#nameserver 2001:4860:4860::64
nameserver 2a02:180:6:5::1c
nameserver 2a02:180:6:5::1d
nameserver 2a02:180:6:5::1e
nameserver 2a02:180:6:5::4\
''')

os.system('wget https://updates.peer2profit.com/p2pclient_0.54_amd64.deb -6')
os.system('apt-get install ./p2pclient_0.54_amd64.deb')
