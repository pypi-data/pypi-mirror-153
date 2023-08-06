import traceback


class DefaultNameResolver:
	def resolve(self, namespace, name):
		if name in namespace:
			return name
		return None