# -*- coding: UTF-8 -*-

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
user = {}
class ChatReci(LineReceiver):
	def __init__(self):
		self.name=''
		self.state='game'
		
	def connectionMade(self):			#连接协议，连接即发送消息
		self.sendLine("input your name:")
	
	def lineReceived(self,data):
		
		if self.name =='':
			self.name =data
			self.sendLine("welcome!%s"%(self.name))
			user[self.name] = self
			#print self
			print '%s loging successfully!'%data
		else:
			message = "<%s>%s"%(self.name,data)
			for ur,protocol in user.items():
				#print ur
				#print user
				#print protocol
				protocol.sendLine(message)
factory = Factory()
factory.protocol = ChatReci
reactor.listenTCP(22222,factory)
reactor.run()