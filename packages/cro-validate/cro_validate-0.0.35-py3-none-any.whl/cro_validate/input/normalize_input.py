import uuid, re, datetime, json
from urllib.parse import urlparse

import cro_validate.api.exception_api as ExceptionApi


def as_truncated_str(name, value, max_len, **kw):
	normalized = as_str(name, value)
	if len(normalized) > max_len:
		normalized = normalized[:max_len] + '...'
	return normalized


def as_instance_of(name, target_obj, target_type, **kw):
	if target_obj is None:
		raise ExceptionApi.create_input_error(name, "Cannot be null (expected instance of type {0})".format(target_type))
	if target_type is None:
		raise ExceptionApi.create_input_error(name, "Cannot be null")
	if isinstance(target_obj, target_type):
		return target_obj
	raise ExceptionApi.create_input_error(
			name,
			'Invalid type.',
			"Must be of type {0} (recieved type '{1}' instead).".format(
					target_type,
					type(target_obj)
				)
		)


def as_int(name, value, **kw):
	try:
		if value is None:
			raise ExceptionApi.create_input_error(name, "Cannot be null")
		if not float(value).is_integer():
			raise ExceptionApi.create_input_error(
					name,
					'Must be integer not float.',
					'Expected integer, received "{0}"'.format(as_truncated_str(name, value, 64))
				)
		return int(value)
	except Exception as ex:
		raise ExceptionApi.create_input_error(
					name,
					'Must be integer.',
					'Expected integer, received "{0}"'.format(type(value)),
					ex
				)


def as_int_within_inclusive_range(name, value, start, end, **kw):
	n = as_int(name, value)
	if n < start:
		raise ExceptionApi.create_input_error(
				name,
				"Must be greater than minimum {0}.".format(start),
				 "Value {0} must be greater than minimum {1}.".format(n, start))
	if n > end:
		raise ExceptionApi.create_input_error(
				name,
				"Must be less than maximum {0}.".format(end),
				"Value {0} must be less than maximum {1}.".format(n, end))
	return n


def as_int_greater_than(name, value, minimum, **kw):
	n = as_int(name, value)
	if n <= minimum:
		raise ExceptionApi.create_input_error(name, "Value {0} must be greater than minimum {1}".format(n, minimum))
	return n


def as_int_greater_than_or_equal_to(name, value, minimum, **kw):
	n = as_int(name, value)
	if n < minimum:
		raise ExceptionApi.create_input_error(name, "Value {0} must be greater than or equal to minimum {1}.".format(n, minimum))
	return n


def as_int_less_than_or_equal_to(name, value, maximum, **kw):
	n = as_int(name, value)
	if n > maximum:
		raise ExceptionApi.create_input_error(name, "Value {0} must be less than or equal to {1}.".format(n, maximum))
	return n


def as_float(name, value, **kw):
	try:
		if value is None:
			raise ExceptionApi.create_input_error(name, "Cannot be None")
		return float(value)
	except Exception:
		raise ExceptionApi.create_input_error(name, 'Must be float')


def as_float_within_inclusive_range(name, value, start, end, **kw):
	n = as_float(name, value)
	if n < start:
		raise ExceptionApi.create_input_error(name, "Value {0} must be greater than minimum {1}.".format(n, start))
	if n > end:
		raise ExceptionApi.create_input_error(name, "Value {0} must be less than maximum {1}.".format(n, end))
	return n


def as_float_greater_than_or_equal_to(name, value, minimum, **kw):
	n = as_float(name, value)
	if n < minimum:
		raise ExceptionApi.create_input_error(name, "Value {0} must be greater than minimum {1}".format(n, minimum))
	return n


def as_float_less_than_or_equal_to(name, value, maximum, **kw):
	n = as_float(name, value)
	if n > maximum:
		raise ExceptionApi.create_input_error(name, "Value {0} must be less than maximum {1}".format(n, maximum))
	return n


def as_float_less_than(name, value, maximum, **kw):
	n = as_float(name, value)
	if n >= maximum:
		raise ExceptionApi.create_input_error(name, "Value {0} must be less than maximum {1}".format(n, maximum))
	return n


def as_str(name, value, **kw):
	try:
		if value is None:
			raise ExceptionApi.create_input_error(name, "Cannot be null")
		if type(value) is bytes:
			return value.decode()
		return str(value)
	except Exception as ex:
		raise ExceptionApi.create_input_error(name, 'Must be string or convertable to type string.', None, ex)


def as_str_with_max_len(name, value, max_len, **kw):
	s = as_instance_of(name, value, str)
	if len(s) > max_len:
		raise ExceptionApi.create_input_error(name, 'Length {0} exceeds max length of {1}.'.format(len(s), max_len))
	return s


def as_str_with_min_len(name, value, min_len, **kw):
	s = as_instance_of(name, value, str)
	if len(s) < min_len:
		raise ExceptionApi.create_input_error(name, 'Length must be at least {1} characters.'.format(len(s), min_len))
	return s


def as_str_within_inclusive_len_range(name, value, min_len, max_len, **kw):
	s = as_str_with_min_len(name, value, min_len)
	s = as_str_with_max_len(name, s, max_len)
	return s


def as_str_with_len(name, value, exact_len, **kw):
	s = s = as_instance_of(name, value, str)
	if len(s) != exact_len:
		raise ExceptionApi.create_input_error(name, "Must be length {0} (length {1} received)".format(exact_len, len(s)))
	return s


def as_str_matching_regex(name, value, rex, flags=None, **kw):
	s = as_instance_of(name, value, str)
	if flags is None:
		flags = 0
	if re.match(rex, s, flags):
		return s
	raise ExceptionApi.create_input_error(name, 'Invalid format.', 'Expression \"{0}\" does not match value \"{1}\"'.format(
			rex,
			value
		))

def _get_one_of_err_desc(name, values, invalid_value, **kw):
	if values is None or len(values) < 1:
		raise ExceptionApi.create_internal_error(
				name,
				'No valid values configured for this value type.'
			)
	desc = 'Must be one of: '
	if len(values) == 1:
		desc = 'Must be: '
	desc = desc + ', '.join(["'{0}'".format(e) for e in values])
	desc = desc + " ('{0}' is invalid)".format(as_truncated_str(name, str(invalid_value), 64))
	return desc


def as_str_in_set(name, value, values, **kw):
	normalized = as_instance_of(name, value, str)
	if value not in values:
		raise ExceptionApi.create_input_error(name, _get_one_of_err_desc(name, values, value))
	return normalized


def as_value_in_set(name, value, values, **kw):
	if value not in values:
		raise ExceptionApi.create_input_error(name, _get_one_of_err_desc(name, values, value))
	return value