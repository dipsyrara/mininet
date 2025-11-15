#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import Node
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def myNetwork():
    net = Mininet(controller=None, link=TCLink)

    info('*** Adding routers\n')
    r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
    r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    r3 = net.addHost('r3', cls=Node, ip='0.0.0.0')

    for r in (r1, r2, r3):
        r.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Adding hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.2/24', defaultRoute='via 10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.2.2/24', defaultRoute='via 10.0.2.1')
    h3 = net.addHost('h3', ip='10.0.4.2/24', defaultRoute='via 10.0.4.1')

    info('*** Creating links\n')
    net.addLink(h1, r1)     
    net.addLink(r1, r2)     
    net.addLink(r2, h2)     
    net.addLink(r2, r3)     
    net.addLink(r3, h3)     

    info('*** Building network\n')
    net.build()

    info('*** Assigning IPs to router interfaces\n')
    
    r1.setIP('10.0.0.1/24', intf='r1-eth0')
    r1.setIP('10.0.1.1/24', intf='r1-eth1')

    r2.setIP('10.0.1.2/24', intf='r2-eth0')
    r2.setIP('10.0.2.1/24', intf='r2-eth1')
    r2.setIP('10.0.3.1/24', intf='r2-eth2')

    r3.setIP('10.0.3.2/24', intf='r3-eth0')
    r3.setIP('10.0.4.1/24', intf='r3-eth1')

    info('*** Setting up static routes\n')

    r1.cmd('ip route add 10.0.2.0/24 via 10.0.1.2')
    r1.cmd('ip route add 10.0.3.0/24 via 10.0.1.2')
    r1.cmd('ip route add 10.0.4.0/24 via 10.0.1.2')

    r2.cmd('ip route add 10.0.0.0/24 via 10.0.1.1')
    r2.cmd('ip route add 10.0.4.0/24 via 10.0.3.2')

    r3.cmd('ip route add 10.0.0.0/24 via 10.0.3.1')
    r3.cmd('ip route add 10.0.1.0/24 via 10.0.3.1')
    r3.cmd('ip route add 10.0.2.0/24 via 10.0.3.1')

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
