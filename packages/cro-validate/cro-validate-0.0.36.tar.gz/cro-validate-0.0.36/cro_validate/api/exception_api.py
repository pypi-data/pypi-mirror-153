import cro_validate.api.configuration_api as ConfigApi


def is_internal_error(ex):
	test = ConfigApi.get_exception_factory().create_internal_error(
			'dummy',
			'test',
			None
		)
	if isinstance(ex, type(test)) is True:
		return True
	return False


def is_input_error(ex):
	test = ConfigApi.get_exception_factory().create_input_error(
			'dummy',
			'test',
			None,
			None
		)
	if isinstance(ex, type(test)) is True:
		return True
	return False


def create_input_error(source, message, internal_message=None, exception=None, **kw):
	return ConfigApi.get_exception_factory().create_input_error(source, message, internal_message, exception, **kw)


def create_internal_error(source, message, exception=None, **kw):
	return ConfigApi.get_exception_factory().create_internal_error(source, message, exception, **kw)