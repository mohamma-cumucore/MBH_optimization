#this is static load balancing for the mobile back haul
# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.

#

# Licensed under the Apache License, Version 2.0 (the "License");

# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at

#

#    http://www.apache.org/licenses/LICENSE-2.0

#

# Unless required by applicable law or agreed to in writing, software

# distributed under the License is distributed on an "AS IS" BASIS,

# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or

# implied.

# See the License for the specific language governing permissions and

# limitations under the License.

 

from ryu.base import app_manager

#from ryu.controller import mac_to_port

from ryu.controller import ofp_event

from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER

from ryu.controller.handler import set_ev_cls

from ryu.ofproto import ofproto_v1_3

#from ryu.ofproto import ofproto_v1_3_parser

from ryu.lib.packet import packet

from ryu.lib.packet import ethernet

from ryu.lib.packet import ether_types

#from ryu.lib import mac 

from ryu.topology.api import get_switch, get_link

#from ryu.app.wsgi import ControllerBase

from ryu.topology import event

import networkx as nx

 

class ProjectController(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
 

    def __init__(self, *args, **kwargs):

        super(ProjectController, self).__init__(*args, **kwargs)

        self.mac_to_port = {}

        self.topology_api_app = self
        
        self.name = 'dynamic_lb'

        self.net=nx.DiGraph()

        self.nodes = {}

        self.links = {}

        self.no_of_nodes = 0

        self.no_of_links = 0

        self.i=0

  

    
    def ls(self,obj):

        print("\n".join([x for x in dir(obj) if x[0] != "_"]))

 

    def add_flow(self, datapath, in_port, dst, actions):

        ofproto = datapath.ofproto

        parser = datapath.ofproto_parser      

        match = datapath.ofproto_parser.OFPMatch( in_port=in_port, eth_dst=dst)

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)] 

        mod = datapath.ofproto_parser.OFPFlowMod(

            datapath=datapath, match=match, cookie=0,

            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,

            priority=1, instructions=inst)

        datapath.send_msg(mod)

 

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures , CONFIG_DISPATCHER)

    def switch_features_handler(self , ev):

         print "swith number",ev.msg.datapath.id,"is added!!"

         datapath = ev.msg.datapath

         ofproto = datapath.ofproto

         parser = datapath.ofproto_parser

         match = parser.OFPMatch()

         actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]

         inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS , actions)]

         mod = datapath.ofproto_parser.OFPFlowMod(

            datapath=datapath, match=match, cookie=0,

            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,

            priority=0, instructions=inst)

         datapath.send_msg(mod)

  

        # add rules to switch s1

         if ev.msg.datapath.id == 1:
             
             ofproto = datapath.ofproto
             parser = datapath.ofproto_parser               
             port_5 = 5
             queue_1 = parser.OFPActionSetQueue(0)
             actions_1 = [queue_1, parser.OFPActionOutput(port_5)]
             port_6 = 6
             queue_2 = parser.OFPActionSetQueue(0)
             actions_2 = [queue_2, parser.OFPActionOutput(port_6)]
             weight_1 = 100
             weight_2 = 100
             watch_port = ofproto_v1_3.OFPP_ANY

             watch_group = ofproto_v1_3.OFPQ_ALL 

             buckets = [

            	parser.OFPBucket(weight_1, watch_port, watch_group, actions_1),             

            	parser.OFPBucket(weight_2, watch_port, watch_group, actions_2)] 

             group_id = 40

             req = parser.OFPGroupMod(

            		datapath, datapath.ofproto.OFPFC_ADD,

            		datapath.ofproto.OFPGT_SELECT, group_id, buckets)

             datapath.send_msg(req)
             
             match = parser.OFPMatch(in_port=3, eth_type=0x0800, ipv4_src="172.16.10.10", ipv4_dst="172.16.60.10",ip_dscp="26")
             match = parser.OFPMatch(in_port=2, eth_type=0x0800, ipv4_src="172.16.20.30", ipv4_dst="172.16.60.10",ip_dscp="26")
             match = parser.OFPMatch(in_port=1, eth_type=0x0800, ipv4_src="172.16.40.20", ipv4_dst="172.16.60.10",ip_dscp="26")
             match = parser.OFPMatch(in_port=4, eth_type=0x0800, ipv4_src="172.16.30.40", ipv4_dst="172.16.60.10",ip_dscp="26")

             actions = [datapath.ofproto_parser.OFPActionGroup(40)]

             inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,

                                             actions)]

             mod = datapath.ofproto_parser.OFPFlowMod(

            	datapath=datapath, match=match, cookie=0,

            	command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,

               	 priority=3, instructions=inst)

             datapath.send_msg(mod)

   

        # adding rules for swith number s4     

         if ev.msg.datapath.id == 4:
             
             ofproto = datapath.ofproto
             
             parser = datapath.ofproto_parser
             
             match = parser.OFPMatch(in_port=1, eth_type=0x0800, ipv4_src="10.0.0.4", ipv4_dst="10.0.0.3")
             
             actions = [parser.OFPActionOutput(2)]
             
             inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
             
             mod = datapath.ofproto_parser.OFPFlowMod(

            	datapath=datapath, match=match, cookie=0,

            	command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,

            	priority=3, instructions=inst)
             datapath.send_msg(mod)

       

        #adding rules to switch number s3

         if ev.msg.datapath.id == 3:
             
             ofproto = datapath.ofproto
             
             parser = datapath.ofproto_parser
             
             match = parser.OFPMatch(in_port=1, eth_type=0x0800, ipv4_src="10.0.0.1", ipv4_dst="10.0.0.3")
             
             match = parser.OFPMatch(in_port=1, eth_type=0x0800, ipv4_src="10.0.0.2", ipv4_dst="10.0.0.3")
             
             actions = [parser.OFPActionOutput(2)]
             
             inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
             
             mod = datapath.ofproto_parser.OFPFlowMod(

            	datapath=datapath, match=match, cookie=0,

            	command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,

            	priority=3, instructions=inst)
             
             datapath.send_msg(mod)

       

        #adding rules to switch number s4

         if ev.msg.datapath.id == 5:          

            ofproto = datapath.ofproto
            parser = datapath.ofproto_parser
            port_1 = 1
            queue_1 = parser.OFPActionSetQueue(0)
            actions_1 = [queue_1, parser.OFPActionOutput(port_1)]
            port_2 = 2
            queue_2 = parser.OFPActionSetQueue(0)
            actions_2 = [queue_2, parser.OFPActionOutput(port_2)]
            weight_1 = 100
            weight_2 = 100
            watch_port = ofproto_v1_3.OFPP_ANY
            watch_group = ofproto_v1_3.OFPQ_ALL 

            buckets = [

            	parser.OFPBucket(weight_1, watch_port, watch_group, actions_1),

            	parser.OFPBucket(weight_2, watch_port, watch_group, actions_2)] 

            group_id = 70 
            
            req = parser.OFPGroupMod(

            		datapath, datapath.ofproto.OFPFC_ADD,

            		datapath.ofproto.OFPGT_SELECT, group_id, buckets)

            datapath.send_msg(req)

            match = parser.OFPMatch(in_port=3, eth_type=0x0800, ipv4_src="10.0.0.3", ipv4_dst="10.0.0.1")
            match = parser.OFPMatch(in_port=3, eth_type=0x0800, ipv4_src="10.0.0.2", ipv4_dst="10.0.0.2")
            match = parser.OFPMatch(in_port=3, eth_type=0x0800, ipv4_src="10.0.0.1", ipv4_dst="10.0.0.3")
           
            actions = [datapath.ofproto_parser.OFPActionGroup(70)]

            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,

                                             actions)]

            mod = datapath.ofproto_parser.OFPFlowMod(

            	datapath=datapath, match=match, cookie=0,

            	command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,

               	 priority=3, instructions=inst)

            datapath.send_msg(mod)

#          	actions = [parser.OFPActionOutput(3)]
#
#          	inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
#
#          	mod = datapath.ofproto_parser.OFPFlowMod(
#
#            datapath=datapath, match=match, cookie=0,
#
#            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
#
#            priority=3, instructions=inst)
#
#          	datapath.send_msg(mod)  

  

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)

    def _packet_in_handler(self, ev):

        msg = ev.msg

        datapath = msg.datapath

        ofproto = datapath.ofproto
        #parser = datapath.ofproto_parser
        in_port = msg.match['in_port'] 

        pkt = packet.Packet(msg.data)

        eth = pkt.get_protocol(ethernet.ethernet) 

        dst = eth.dst

        src = eth.src

        dpid = datapath.id

        self.mac_to_port.setdefault(dpid, {}) 
        #ignore lldp packets
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return            

        if src not in self.net:
            self.net.add_node(src)	   	    
            self.net.add_edge(dpid,src,{'port':in_port})
            self.net.add_edge(src,dpid)
	    #print src in self.net
        if dst in self.net:
            
            path=nx.shortest_path(self.net,src,dst)  

            next=path[path.index(dpid)+1]

            out_port=self.net[dpid][next]['port']            

        else:

            out_port = ofproto.OFPP_FLOOD

 

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time

        if out_port != ofproto.OFPP_FLOOD:

            self.add_flow(datapath, in_port, dst, actions)

 

        out = datapath.ofproto_parser.OFPPacketOut(

            datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,

            actions=actions)

        datapath.send_msg(out)

   

    @set_ev_cls(event.EventSwitchEnter)

    def get_topology_data(self, ev):

        switch_list = get_switch(self.topology_api_app, None)  

        switches = [switch.dp.id for switch in switch_list]

        self.net.add_nodes_from(switches)       

        print '#### The Switches added are ###'

        for switch in switch_list:
         
          print switch       

        links_list = get_link(self.topology_api_app, None)    

        links=[(link.src.dpid,link.dst.dpid,{'port':link.src.port_no}) for link in links_list]

        #print links

        self.net.add_edges_from(links)

        links=[(link.dst.dpid,link.src.dpid,{'port':link.dst.port_no}) for link in links_list]

        #print links

        self.net.add_edges_from(links)

        print "**********List of links"

        print self.net.edges()
