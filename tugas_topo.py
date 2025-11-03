#!/usr/bin/python3

"""
Skrip Mininet untuk membuat topologi router tradisional berdasarkan
gambar 'image_eab03e.png'.

Topologi:
h1 (10.0.0.2/24) -- r1 -- (10.0.1.0/24) -- r2 -- (10.0.3.0/24) -- r3 -- (10.0.4.0/24) -- h3 (10.0.4.2/24)
                                             |
                                        (10.0.2.0/24)
                                             |
                                        h2 (10.0.2.2/24)
"""

from mininet.net import Mininet
from mininet.node import Node
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class LinuxRouter( Node ):
    """Node yang dikonfigurasi sebagai Router Linux."""
    def config( self, **params ):
        super( LinuxRouter, self ).config( **params )
        self.cmd( 'sysctl -w net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl -w net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


def runTopology():
    "Membuat dan menjalankan topologi router"
    
    net = Mininet( topo=None,
                   build=False,
                   link=TCLink,
                   controller=None ) 

    info( '*** Menambahkan Host (h1, h2, h3)\n' )
    h1 = net.addHost( 'h1', ip='10.0.0.2/24', defaultRoute='via 10.0.0.1' )
    h2 = net.addHost( 'h2', ip='10.0.2.2/24', defaultRoute='via 10.0.2.1' )
    h3 = net.addHost( 'h3', ip='10.0.4.2/24', defaultRoute='via 10.0.4.1' )

    info( '*** Menambahkan Router (r1, r2, r3)\n' )
    r1 = net.addHost( 'r1', cls=LinuxRouter )
    r2 = net.addHost( 'r2', cls=LinuxRouter )
    r3 = net.addHost( 'r3', cls=LinuxRouter )

    info( '*** Membuat Links\n' )
    net.addLink( h1, r1, intfName1='h1-eth0', intfName2='r1-eth0', params2={ 'ip' : '10.0.0.1/24' } )
    net.addLink( h2, r2, intfName1='h2-eth0', intfName2='r2-eth2', params2={ 'ip' : '10.0.2.1/24' } )
    net.addLink( h3, r3, intfName1='h3-eth0', intfName2='r3-eth1', params2={ 'ip' : '10.0.4.1/24' } )

    net.addLink( r1, r2, intfName1='r1-eth1', params1={ 'ip' : '10.0.1.1/24' },
                         intfName2='r2-eth0', params2={ 'ip' : '10.0.1.2/24' } )
    
    net.addLink( r2, r3, intfName1='r2-eth1', params1={ 'ip' : '10.0.3.1/24' },
                         intfName2='r3-eth0', params2={ 'ip' : '10.0.3.2/24' } )

    info( '*** Memulai Jaringan\n' )
    net.build()
    
    info( '*** Mengkonfigurasi Static Routes di Router\n' )
    
    r1.cmd( 'ip route add 10.0.2.0/24 via 10.0.1.2' )
    
    r1.cmd( 'ip route add 10.0.4.0/24 via 10.0.1.2' )
    
    r1.cmd( 'ip route add 10.0.3.0/24 via 10.0.1.2' )

    r2.cmd( 'ip route add 10.0.0.0/24 via 10.0.1.1' )

    r2.cmd( 'ip route add 10.0.4.0/24 via 10.0.3.2' )

    
    r3.cmd( 'ip route add 10.0.0.0/24 via 10.0.3.1' )
    
    r3.cmd( 'ip route add 10.0.2.0/24 via 10.0.3.1' )

    r3.cmd( 'ip route add 10.0.1.0/24 via 10.0.3.1' )

    info( '*** Menjalankan Tes Ping (h1 -> h2, h1 -> h3)\n' )

    ping_h1_h2 = h1.cmd( 'ping -c 3 %s' % h2.IP() )
    info( ping_h1_h2 )

    ping_h1_h3 = h1.cmd( 'ping -c 3 %s' % h3.IP() )
    info( ping_h1_h3 )

    info( '*** Menjalankan CLI\n' )
    CLI( net )

    info( '*** Menghentikan Jaringan\n' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    runTopology()