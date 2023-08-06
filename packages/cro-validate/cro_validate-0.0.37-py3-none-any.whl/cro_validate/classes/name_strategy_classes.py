

class NameStrategy:
	def create_name(self, **kw):
		raise NotImplementedError()

	def to_json(self):
		return {}


class DefaultDefinitionNameStrategy(NameStrategy):
	def create_name(self, definition, input_name):
		if input_name is None:
			if definition.is_object():
				return definition.data_format.model_name
			elif definition.is_array():
				return definition.data_format + 'Array'
		return input_name

	def get_fqn(self, namespace, field_name):
		if namespace is not None and len(namespace) > 0:
			return namespace + '.' + field_name
		return field_name


	def get_parent_fqn(self, fqn):
		index = fqn.rfind('.')
		if index < 0:
			return ''
		return fqn[:index]


	def get_field_name_from_fqn(self, fqn):
		index = fqn.rfind('.')
		if index < 0:
			return ''
		return fqn[index+1:]


class DefaultComponentNameStrategy(NameStrategy):
	def create_component_name(snake_case_name, suffix):
		# create_component_name('my_name_my_suff', 'MySuff') => MyNameSuff
		# create_component_name('my_name', 'MySuff') => MyNameSuff
		class MatchState:
			def __init__(self, start):
				self.start = start
				self.cur_index = -1

		# Class Name
		############
		class_name = None
		i = 0
		while i < len(snake_case_name):
			c = snake_case_name[i]
			if class_name is None:
				class_name = c.upper()
			elif c in {'_', '-', '.'}:
				i = i + 1
				class_name = class_name + snake_case_name[i].upper()
			else:
				class_name = class_name + c		
			i = i + 1

		# Suffix Overlap
		################
		states = []
		i = 0
		normalized_class_name = class_name.lower()
		normalized_suffix = suffix.lower()
		while i < len(normalized_class_name):
			c = normalized_class_name[i]
			if c == normalized_suffix[0]:
				states.append(MatchState(i))
			matches = []
			for state in states:
				state.cur_index = state.cur_index + 1
				if state.cur_index >= len(normalized_suffix):
					continue
				if normalized_class_name[state.start + state.cur_index] != normalized_suffix[state.cur_index]:
					continue
				matches.append(state)
			states = matches
			i = i + 1

		# Append Overlap
		################
		match = None
		for state in states:
			if state.start + state.cur_index + 1 != len(normalized_class_name):
				continue
			if state.cur_index < 2:
				continue
			match = state
			break
		if match is not None:
			return class_name[:match.start] + suffix
		return class_name + suffix

	def create_name(self, definition, suffix='Model', display_name=None):
		if definition.is_object():
			return definition.meta.schema_name
		if definition.is_array():
			return definition.data_format
		if display_name is None:
			display_name = definition.name
		result = DefaultComponentNameStrategy.create_component_name(display_name, suffix)
		return result