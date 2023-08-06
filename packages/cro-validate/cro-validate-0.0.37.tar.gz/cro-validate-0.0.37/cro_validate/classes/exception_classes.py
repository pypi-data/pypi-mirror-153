

class DefaultExceptionFactory:
	def create_input_error(self, source, message, internal_message=None, exception=None, **kw):
		return ValueError(str(source) + ': ' + str(message))

	def create_internal_error(self, source, message, exception=None, **kw):
		return SystemError(str(source) + ': ' + str(message))