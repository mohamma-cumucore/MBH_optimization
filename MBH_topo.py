"""this the sample topology  for the Mobile Back haul

It has 5 switches teporarily interconnected to each other

  eNBs --- switch --- switch
	      -	         -		-
		-      -			   -
		   -			           switch ----MBH
		 -    -			
	       -		-	    -
  eNBs --- switch --- switch

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mbh_topos' from the command line.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
class MBH_topo( Topo ):
    "Simple topology example."

    def __init__( self, **opts ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self,**opts )

        # Add hosts and switches
        topHost_h11 = self.addHost( 'URLL',ip="172.16.10.10/24",mac ="00:00:00:00:00:01" )
        topHost_h12 = self.addHost( 'LBWIoT',ip="172.16.10.30/24",mac ="00:00:00:00:00:03" )
        topHost_h13 = self.addHost('BE',ip="172.16.10.20/24",mac ="00:00:00:00:00:02")
        topHost_h14 = self.addHost('MBB',ip="172.16.10.40/24",mac ="00:00:00:00:00:04")        
	#bottomHost_h21 = self.addHost( 'h21' )
        #bottomHost_h22 = self.addHost( 'h22' )
        Server = self.addHost( 'Server',ip="172.16.10.50/24",mac ="00:00:00:00:00:05" )
        front_top_Switch = self.addSwitch( 's1' )
        #front_bottom_Switch = self.addSwitch( 's2' )
        middle_top_Switch = self.addSwitch( 's3' )
        middle_bottom_Switch = self.addSwitch( 's4' )
        back_Switch = self.addSwitch( 's5' )    
    # Add links
        self.addLink( topHost_h11, front_top_Switch )
        self.addLink( topHost_h12, front_top_Switch )
        self.addLink( topHost_h13, front_top_Switch ) 
        self.addLink( topHost_h14, front_top_Switch ) 
        self.addLink( front_top_Switch, middle_top_Switch)
        self.addLink( front_top_Switch, middle_bottom_Switch )
	#self.addLink( front_bottom_Switch, middle_top_Switch )
	#self.addLink( front_bottom_Switch, middle_bottom_Switch )
	self.addLink( middle_top_Switch, back_Switch )
	self.addLink( middle_bottom_Switch, back_Switch )
	self.addLink( back_Switch,  Server)        
        #self.addLink( front_bottom_Switch, bottomHost_h21 )
	#self.addLink( front_bottom_Switch, bottomHost_h22 )



topos = { 'mbh_topo': ( lambda: MBH_topo() ) }
