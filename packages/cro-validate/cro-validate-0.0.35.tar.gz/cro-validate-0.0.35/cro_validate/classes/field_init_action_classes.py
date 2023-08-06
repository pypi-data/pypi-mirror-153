import re

from cro_validate.classes.configuration_classes import Config

class SetFieldsRequired:
	def __init__(self, required=True, field_list=None, pattern=None, **kw):
		self.required=required
		self.field_list = set()
		self.pattern = pattern
		if field_list is not None:
			self.field_list.update(field_list)

	def __call__(self, field_name, field):
		if field_name in self.field_list:
			field.required = self.required
		if self.pattern is not None:
			if re.match(self.pattern, field_name) is not None:
				field.required = self.required
		return field


class OmitFields:
	def __init__(self, field_list=None, field_white_list=None, pattern=None, **kw):
		self.field_list = set()
		self.field_white_list = set()
		self.pattern = pattern
		if field_list is not None:
			self.field_list.update(field_list)
		if field_white_list is not None:
			self.field_white_list.update(field_white_list)

	def __call__(self, field_name, field):
		if field_name in self.field_white_list:
			return field
		if field_name in self.field_list:
			return None
		if self.pattern is not None:
			if re.match(self.pattern, field_name) is not None:
				return None
		return field
