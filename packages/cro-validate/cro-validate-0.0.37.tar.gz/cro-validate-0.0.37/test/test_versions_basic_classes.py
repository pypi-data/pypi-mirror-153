


class TestModelVerConv_v0:
	def increment(self, fqn, definition, value):
		value['d'] = True
		return value

	def decrement(self, fqn, definiton, value):
		raise Exception('Not Implemented')


class TestModelVerConv_v1:
	def increment(self, fqn, definition, value):
		del value['b']
		return value

	def decrement(self, fqn, definiton, value):
		del value['d']
		del value['c']
		return value
