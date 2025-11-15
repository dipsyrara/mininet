#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Node
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def myNetwork():

    net = Mininet(topo=None, build=False, ipBase='10.0.0.0/8')

    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    r1 = net.addHost('r1', cls=Node)
    
    h1 = net.addHost('h1', ip='10.0.1.10/24', defaultRoute='via 10.0.1.1')
    h2 = net.addHost('h2', ip='10.0.2.10/24', defaultRoute='via 10.0.2.1')

    net.addLink(r1, s1, intfName1='r1-eth1')
    net.addLink(r1, s2, intfName1='r1-eth2')

    net.addLink(s1, h1)
    net.addLink(s2, h2)

    net.start()

    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    r1.cmd('ip addr flush dev r1-eth1') 
    r1.cmd('ip addr add 10.0.1.1/24 dev r1-eth1')
    r1.cmd('ip link set r1-eth1 up')
    
    r1.cmd('ip addr flush dev r1-eth2') 
    r1.cmd('ip addr add 10.0.2.1/24 dev r1-eth2')
    r1.cmd('ip link set r1-eth2 up')

    s1.start([])
    s2.start([])

    s1.cmd('ovs-ofctl add-flow s1 "priority=1,actions=normal"')
    s2.cmd('ovs-ofctl add-flow s2 "priority=1,actions=normal"')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()