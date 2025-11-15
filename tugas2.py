#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Node
from mininet.node import OVSController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def myNetwork():

    net = Mininet(topo=None, build=False, ipBase='10.0.0.0/8',
                  controller=OVSController)

    info('*** Adding controller\n')
    c0 = net.addController('c0')

    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    info('*** Add router (r1)\n')
    r1 = net.addHost('r1', cls=Node)
    
    info('*** Add hosts\n')
    h1 = net.addHost('h1', ip='10.0.1.10/24', defaultRoute='via 10.0.1.1')
    h2 = net.addHost('h2', ip='10.0.2.10/24', defaultRoute='via 10.0.2.1')

    info('*** Add links\n')
    net.addLink(r1, s1, intfName1='r1-eth1')
    net.addLink(r1, s2, intfName1='r1-eth2')

    net.addLink(s1, h1)
    net.addLink(s2, h2)

    info('*** Starting network\n')
    net.start()

    info('*** Configuring Router r1\n')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    r1.cmd('ip addr flush dev r1-eth1') 
    r1.cmd('ip addr add 10.0.1.1/24 dev r1-eth1')
    r1.cmd('ip link set r1-eth1 up')
    
    r1.cmd('ip addr flush dev r1-eth2') 
    r1.cmd('ip addr add 10.0.2.1/24 dev r1-eth2')
    r1.cmd('ip link set r1-eth2 up')


    info('*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()