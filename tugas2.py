#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    # Membuat jaringan kosong tanpa topologi bawaan
    net = Mininet(topo=None, build=False, ipBase='10.0.0.0/8')

    info('*** Adding controller\n')

    info('*** Add switches\n')
    # Switch bertipe OVS Kernel
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    # Router menggunakan Host Node dan diaktifkan IP forwarding (fungsi Routing L3)
    r1 = net.addHost('r1', cls=Node)
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')      # <- Perbedaan coding: routing aktif

    info('*** Add hosts\n')
    # Host berada di subnet berbeda dan diarahkan ke gateway router
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.10/24', defaultRoute='via 10.0.1.1')
    h2 = net.addHost('h2', cls=Host, ip='10.0.2.10/24', defaultRoute='via 10.0.2.1')

    info('*** Add links\n')
    # Router ke Switch (beda interface)
    net.addLink(r1, s1, intfName1='r1-eth1')
    net.addLink(r1, s2, intfName1='r1-eth2')

    # Switch ke Host
    net.addLink(s1, h1)
    net.addLink(s2, h2)

    info('*** Starting network\n')
    net.build()

    # Memberikan IP ke Router (gateway)
    r1.cmd('ip addr add 10.0.1.1/24 dev r1-eth1')
    r1.cmd('ip link set r1-eth1 up')
    r1.cmd('ip addr add 10.0.2.1/24 dev r1-eth2')
    r1.cmd('ip link set r1-eth2 up')

    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    # Switch berjalan tanpa controller (standalone)
    net.get('s1').start([])
    net.get('s2').start([])

    info('*** Installing flow rules for L2 functionality\n')
    # Flow "normal" = perbedaan coding: membuat switch bekerja sebagai switch Layer 2 otomatis
    s1.cmd('ovs-ofctl add-flow s1 "priority=1,actions=normal"')
    s2.cmd('ovs-ofctl add-flow s2 "priority=1,actions=normal"')

    # Perbedaan coding L2 vs L3:
    # - L2: Switch menggunakan actions=normal
    # - L3: Router mengaktifkan IP forwarding dan diberi IP tiap interface

    info('*** Post configure switches and hosts\n')

    # Menjalankan CLI Mininet untuk test
    CLI(net)
    net.stop()

if _name_ == '_main_':
    setLogLevel('info')
    myNetwork()