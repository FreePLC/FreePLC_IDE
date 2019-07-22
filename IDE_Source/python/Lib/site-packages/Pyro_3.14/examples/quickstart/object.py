
class myObject(object):
	def method1(s, string):
		return "Your string length is: "+str(len(string))
	def method2(s, number):
		return "The square of your number is: "+str(number*number)

def remote_objects():
    return { 'quickstart': myObject() }
