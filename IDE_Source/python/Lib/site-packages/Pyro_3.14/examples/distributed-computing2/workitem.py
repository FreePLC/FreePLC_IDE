class Workitem(object):
	def __init__(self, itemId, data):
		print "Created workitem",itemId # XXX
		self.itemId=itemId
		self.data=data
		self.result=None
		self.processedBy=None
	def __str__(self):
		return "<Workitem id=%s>" % str(self.itemId)
