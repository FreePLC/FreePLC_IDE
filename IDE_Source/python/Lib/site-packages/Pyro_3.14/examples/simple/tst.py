
# These classes will be remotely accessed.


class testclass(object):
	def mul(s, arg1, arg2): return arg1*arg2
	def add(s, arg1, arg2): return arg1+arg2
	def sub(s, arg1, arg2): return arg1-arg2
	def div(s, arg1, arg2): return arg1/arg2
	def error(s):
		x=foo()
		x.crash()

class foo(object):
	def crash(s):
		s.crash2('going down...')
	def crash2(s, arg):
		# this statement will crash on purpose:
		x=arg/2
