#!/usr/bin/python2.7 -tt

class DbpediaNode:
	"""
	must have only two attributes 
	type 
	data
	"""
	def	__init__(self, **kwargs):
			self.variables = kwargs

	
	def	__repr__(self):
			str = '{'
			for k in self.variables.keys():
				str += '\''+k+'\''+': '+'\''+self.variables[k]+'\''+','
			str = str[:-1]+'}'
			return str


	def	__str__(self):
			str = '{'
			for k in self.variables.keys():
				str += '\''+k+'\''+': '+'\''+self.variables[k]+'\''+','
			str = str[:-1]+'}'
			return str


	def	get_variable(self, name):
			return self.variables.get(name,None)

	
	def	set_variable(self, name, vale):
			self.variables[name] = value


def	test():
		node = DbpediaNode(type='url',data='http://google.com', face='google')
		l = []
		l = l.append(node)
		l = l.append(node)
		print(l)	


if __name__ == '__main__':
	test()	
