
# this module contains the ShoppingAgent code

class ShoppingAgent(object):
	def __init__(self, name):
		self.name=name
		self.productsToBuy=[]
		self.productsBought={}
		self.boughtObjects=[]
		self.cash=0
		self.shopsVisited=0
	def shoppingList(self, products):
		self.productsToBuy=products
	def cashLimit(self,cash):
		self.cash=cash
	def visitShop(self, shop):
		print self.name,'is visiting',shop.name
		self.shopsVisited+=1
		goods = shop.getStock()
		for p in self.productsToBuy[:]:
			if goods.has_key(p):
				price = goods[p]
				if price<=self.cash:
					self.cash-=price
					# buy an object from the shop
					object=shop.buy(self,p)
					# The object is "the real thing"; an instance.
					# store it in our pockets. We will return with
					# this to the client.
					self.boughtObjects.append(object)
					self.productsBought[p]=shop.name
					self.productsToBuy.remove(p)
	def result(self):
		print 'My name is',self.name
		print '  I have bought:'
		for p in self.productsBought.keys():
			print '\t',p,'('+self.productsBought[p]+')'
		print '  I couldn\'t buy:',
		for p in self.productsToBuy:
			print p,
		print '\n  Cash left:',self.cash,
		print 'after visiting',self.shopsVisited,'shops'
	def describeObjects(self):
		print "Now describing the objects I've bought:"
		for obj in self.boughtObjects:
			# notice that these use the actual objects
			# transferred from the server to the client!
			print ' ',obj.getName(),'-',obj.getDescription()
		if not self.boughtObjects:
			print "I've got nothing..."
	def __str__(self):
		return self.name
		
