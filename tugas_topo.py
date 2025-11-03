#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import Node
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class LinuxRouter( Node ):
    def config( self, **params ):
        super( LinuxRouter, self ).config( **params )
        self.cmd( 'sysctl -w net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl -w net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

def myNetwork():
    net = Mininet(controller=None, link=TCLink)

    r1 = net.addHost('r1', cls=LinuxRouter)
    r2 = net.addHost('r2', cls=LinuxRouter)
    r3 = net.addHost('r3', cls=LinuxRouter)

    h1 = net.addHost('h1', ip='10.0.0.2/24', defaultRoute='via 10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.2.2/24', defaultRoute='via 10.0.2.1')
    h3 = net.addHost('h3', ip='10.0.4.2/24', defaultRoute='via 10.0.4.1')

    # Link dengan konfigurasi IP in-line
    net.addLink(h1, r1, intfName2='r1-eth0', params2={'ip': '10.0.0.1/24'})
    net.addLink(h2, r2, intfName2='r2-eth1', params2={'ip': '10.0.2.1/24'})
    net.addLink(h3, r3, intfName2='r3-eth1', params2={'ip': '10.0.4.1/24'})

    net.addLink(r1, r2, intfName1='r1-eth1', params1={'ip': '10.0.1.1/24'},
                        intfName2='r2-eth0', params2={'ip': '10.0.1.2/24'})
    
    net.addLink(r2, r3, intfName1='r2-eth2', params1={'ip': '10.0.3.1/24'},
                        intfName2='r3-eth0', params2={'ip': '10.0.3.2/24'})

    net.build()

    # Rute statis ditambahkan setelah network di-build
    r1.cmd('ip route add 10.0.2.0/24 via 10.0.1.2')
    r1.cmd('ip route add 10.0.3.0/24 via 10.0.1.2')
    r1.cmd('ip route add 10.0.4.0/24 via 10.0.1.2')

    r2.cmd('ip route add 10.0.0.0/24 via 10.0.1.1')
    r2.cmd('ip route add 10.0.4.0/24 via 10.0.3.2')

    r3.cmd('ip route add 10.0.0.0/24 via 10.0.3.1')
    r3.cmd('ip route add 10.0.1.0/24 via 10.0.3.1')
    r3.cmd('ip route add 10.0.2.0/24 via 10.0.3.1')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
