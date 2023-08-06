

class ClassName:
	def class_fqn(obj):
		return '.'.join([obj.__class__.__module__, obj.__class__.__name__])

	def class_fqn_parts(fqn):
		i = fqn.rfind('.')
		m = fqn[:i]
		c = fqn[i+1:]
		return (m, c)


class Empty:
	def isempty(v):
		if isinstance(v, Empty):
			return True
		if v is Empty:
			return True
		return False


class Omitted:
	def is_omitted(v):
		if isinstance(v, Omitted):
			return True
		if v is Omitted:
			return True
		return False


class Boundaries:
	def get_str_min_len_boundary(min_len, c='a'):
		if min_len < 1:
			return []
		boundary = ''.join([c for i in range(min_len - 1)])
		return [boundary]

	def get_str_max_len_boundary(max_len, c='a'):
		if max_len < 1:
			return []
		boundary = ''.join([c for i in range(max_len + 1)])
		return [boundary]


class VersionMutation:
	def __init__(self, action, config, description):
		self.action = action
		self.config = config
		self.description = description

	def __str__(self):
		return '<VersionMutation action={0}, desc={1}, config={2}>'.format(
				self.action,
				self.description,
				self.config
			)

	def __repr__(self):
		return self.__str__()
