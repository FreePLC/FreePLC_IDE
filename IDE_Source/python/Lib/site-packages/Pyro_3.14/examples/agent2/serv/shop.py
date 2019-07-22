# The actual shop.
# Shopping agents come here to fill their pockets.

class Mall(object):
	def __init__(self):
		self.shops=[]
	def addShop(self,shop):
		self.shops.append(shop)
	def goShopping(self, shopper):
		for shop in self.shops:
			shopper.visitShop(shop)
		return shopper			# !!! return agent to client !!!
	def __call__(self):
		return self				# hack for testserver's delegation init


class Shop(object):
	def __init__(self,name):
		self.name=name
		self.stock={}
	def setStock(self,stock):
		self.stock=stock
	def getStock(self):
		return self.stock
	def buy(self,shopper,product):
		if self.stock.has_key(product):
			print self.name+':',shopper,'buys',product
			del self.stock[product]
			# Create a "true" object that was bought.
			# The shopping agent will put this object
			# in his inventory, so it will travel back
			# to the client (also by using mobile code).
			exec("import objects."+product)
			object=eval("objects."+product+"."+product+"()")
			return object

