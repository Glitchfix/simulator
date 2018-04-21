"""
@package p2psp-simulator
splitter_dbs module
"""

# DBS (Data Broadcasting Set) layer

# DBS is the most basic layer to provide communication among splitter
# (source of the stream) and peers (destination of the stream), using
# unicast transmissions. The splitter sends a different chunk of
# stream to each peer, using a random round-robin scheduler.

# TODO: In each round peers are selected at random, but all peers are
# sent a chunk, in a round).

from .common import Common
from threading import Thread
from threading import Lock
import time
from .simulator_stuff import Simulator_stuff
from .simulator_stuff import Simulator_socket as socket
#from .simulator_stuff import lg
import sys
import struct
import logging

class Tracker(Simulator_stuff):
	lg = logging.getLogger(__name__)
	def __init__(self,s="T"):
		self.s = s
		self.alive=True
		self.splitter_list=[]
    
	def setup_tracker_connection_socket(self):
		self.tracker_connection_socket = socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.tracker_connection_socket.bind(self.s)
		self.tracker_connection_socket.listen(1)
    
	def handle_conn_arrival(self, connection):
		serve_socket = connection[0]
		incoming_peer = connection[1]
		
		self.lg.info("{}: accepted connection from peer {}".format(self.s, incoming_peer))
		
		msg,peer = serve_socket.recv(1024)
		print(msg,peer)
		if msg=="*PT":
			print("Tracker received"+msg)
			msg=splitter_id()
			peer=incoming_peer
		elif msg[:3]=="*ST":
			print("Tracker received"+msg)
			self.add_splitter(msg[3:])
			msg="SPJ"
			peer=msg[3:]
		self.lg.info("Tracker {}: received {} from {}".format(self.s, msg, incoming_peer))

		serve_socket.send(msg)
		# S I M U L A T I O N
		Simulator_stuff.FEEDBACK["DRAW"].put(("O", "Node", "IN", incoming_peer))
		'''
		if (incoming_peer[0] == "P"):
			msg="*"+splitter_id()
			self.lg.info("{}: received {} from {}".format(self.s, msg,peer))
			self.serve_socket.sendto(msg, peer)
		elif (incoming_peer[0] == "S"):
			add_splitter(incoming_peer)
			serve_socket.close()'''
			

	def handle_arrivals(self):
		while self.alive:
			serve_socket, peer = self.tracker_connection_socket.accept()
			serve_socket = socket(sock=serve_socket)
			#peer_serve_socket.set_id(peer)	
			self.lg.info("{}: connection from {}".format(self.s, peer))
			Thread(target=self.handle_conn_arrival, args=((serve_socket, peer),)).start()
        
	def send_chunk(self, chunk_msg, peer):
		#self.lg.info("splitter_dbs.send_chunk({}, {})".format(chunk_msg, peer))
		msg = struct.pack("is6s", *chunk_msg)
        #msg = struct.pack("is3s", chunk_msg[0], bytes(chunk_msg[1]), chunk_msg[2])
		self.team_socket.sendto(msg, peer)
    
	def add_splitter(self,new_splitter):
		self.splitter_list=new_splitter+self.splitter_list

	def splitter_id(self):
		s=self.splitter[0]
		self.splitter_list=self.splitter_list[:1]+self.splitter_list[1:]
		return s
	
	def run(self):
		self.setup_tracker_connection_socket()
		#self.setup_team_socket()
		Thread(target=self.handle_arrivals).start()
		#Thread(target=self.add_splitter).start()
		#Thread(target=self.splitter_id).start()
		
